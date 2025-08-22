# accounts/models.py

from django.conf import settings
from django.db import models

class EmailOTPDevice(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_otp_device'
    )
    is_confirmed = models.BooleanField(default=False)
    secret_code = models.CharField(max_length=6, null=True, blank=True)
    last_generated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Email OTP Device"