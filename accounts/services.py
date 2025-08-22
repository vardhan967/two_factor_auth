# accounts/services.py

import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .models import EmailOTPDevice


def generate_otp() -> str:
    """Generates a 6-digit random OTP."""
    return str(random.randint(100000, 999999))


def send_otp_email(user) -> None:
    """Generates an OTP, saves it, and emails it to the user using Gmail SMTP."""
    device, _ = EmailOTPDevice.objects.get_or_create(user=user)

    otp_code = generate_otp()
    device.secret_code = otp_code
    device.last_generated_at = timezone.now()
    device.save()

    # Debug log
    print(f"--- DEBUG: Sending OTP email with code: {otp_code} for user: {user.username} ---")

    # Prepare context for template
    context = {
        'user': user,
        'otp_code': otp_code,
    }

    # Render the HTML template
    html_content = render_to_string('accounts/otp_email.html', context)
    text_content = f"Hello {user.username},\n\nYour verification code is: {otp_code}\nIt will expire in 10 minutes."

    # Send email via Gmail SMTP
    email = EmailMultiAlternatives(
        subject="Your Two-Factor Authentication Code",
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


def validate_otp(user, otp_code: str) -> bool:
    """Validates the OTP provided by the user."""
    try:
        device = user.email_otp_device
    except EmailOTPDevice.DoesNotExist:
        return False

    if (timezone.now() - device.last_generated_at) > timedelta(minutes=10):
        return False

    if device.secret_code == otp_code:
        device.secret_code = None
        device.save()
        return True

    return False
