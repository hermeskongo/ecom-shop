from django.urls import path

from accounts.views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserActivationView,
    UserDashboardView,
    UserForgotPassword, UserResetValidateView, UserResetPassword, UserDashboardOrdersView, UserDashboardChangeProfile,
    UserDashboardChangePassword, UserDashboardOrderDetails
)

app_name = 'accounts'

urlpatterns = [
    path('accounts/register/', UserRegistrationView.as_view(), name='register'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    
    path('accounts/dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('accounts/dashboard/orders/', UserDashboardOrdersView.as_view(), name='dashboard_orders'),
    path('accounts/dashboard/order/<int:pk>/details/', UserDashboardOrderDetails.as_view(), name='order_details'),
    path('accounts/dashboard/profile/', UserDashboardChangeProfile.as_view(), name='dashboard_profile'),
    path('accounts/dashboard/password/', UserDashboardChangePassword.as_view(), name='dashboard_password'),
    
    path('accounts/activate/<uidb64>/<token>', UserActivationView.as_view(), name='activation'),
    
    path('accounts/forgot_password/', UserForgotPassword.as_view(), name='forgot_password'),
    path('accounts/reset_password_validate/<uidb64>/<token>', UserResetValidateView.as_view(), name='reset_password_validate'),
    path('accounts/reset_password/', UserResetPassword.as_view(), name='reset_password'),
]
