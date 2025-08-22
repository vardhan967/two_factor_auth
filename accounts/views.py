# accounts/views.py

from django.contrib.auth import authenticate, login, get_user_model,logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from . import services
from .models import EmailOTPDevice
from .tokens import account_activation_token

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([username, email, password]):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        activation_link = f"http://localhost:8080/activate/{uid}/{token}" # Use your frontend port

        # --- THIS IS THE UPDATED EMAIL LOGIC ---
        context = {
            'user': user,
            'activation_link': activation_link,
        }
        html_content = render_to_string('accounts/activation_email.html', context)
        text_content = f"Hello {user.username},\n\nPlease click the link to activate your account:\n{activation_link}"
        
        email_message = EmailMultiAlternatives(
            subject='Activate Your Account',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send()
        # --- END OF UPDATE ---

        return Response(
            {'message': 'Registration successful. Please check your email to activate your account.'},
            status=status.HTTP_201_CREATED
        )

@method_decorator(csrf_exempt, name='dispatch')
class ActivateAccountView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully. You can now log in.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Activation link is invalid or has expired.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({'error': 'Please confirm your email to activate your account.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            if user.email_otp_device.is_confirmed:
                request.session['unverified_user_id'] = user.id
                services.send_otp_email(user)
                return Response({'message': '2FA required. OTP sent to email.'}, status=status.HTTP_200_OK)
        except EmailOTPDevice.DoesNotExist:
            pass 

        login(request, user)
        
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_2fa_enabled': hasattr(user, 'email_otp_device') and user.email_otp_device.is_confirmed,
                'is_active': user.is_active,
                'date_joined': user.date_joined,
            }
        }, status=status.HTTP_200_OK)

class Verify2FAView(APIView):
    def post(self, request):
        otp_code = request.data.get('otp_code')
        user_id = request.session.get('unverified_user_id')

        if not user_id:
            return Response({'error': 'No user to verify'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        if services.validate_otp(user, otp_code):
            login(request, user)
            del request.session['unverified_user_id']
            return Response({'message': '2FA verification successful. Logged in.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

class Enable2FAView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        services.send_otp_email(request.user)
        return Response({'message': 'OTP sent to your email to confirm 2FA setup.'}, status=status.HTTP_200_OK)

class Verify2FASetupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        otp_code = request.data.get('otp_code')
        if services.validate_otp(request.user, otp_code):
            device = request.user.email_otp_device
            device.is_confirmed = True
            device.save()
            return Response({'message': '2FA has been enabled successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_2fa_enabled': hasattr(user, 'email_otp_device') and user.email_otp_device.is_confirmed,
        'is_active': user.is_active,
        'date_joined': user.date_joined,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    def get(self, request):
        return Response({'message': 'CSRF cookie set'})