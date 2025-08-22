# two_factor_auth/accounts/urls.py

from django.urls import path
from .views import logout_view 
from .views import (
    RegisterView, 
    ActivateAccountView,
    LoginView, 
    Verify2FAView, 
    Enable2FAView, 
    Verify2FASetupView,
    get_current_user,
    GetCSRFToken,
)

urlpatterns = [
    # The path that is causing the 404 error
    path('user/', get_current_user, name='current-user'), 
    
    path('csrf/', GetCSRFToken.as_view(), name='csrf-token'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate-account'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-2fa/', Verify2FAView.as_view(), name='verify-2fa'),
    path('enable-2fa/', Enable2FAView.as_view(), name='enable-2fa'),
    path('verify-2fa-setup/', Verify2FASetupView.as_view(), name='verify-2fa-setup'),
    path('logout/', logout_view, name='logout'),
]