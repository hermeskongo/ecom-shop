from django.urls import path

from accounts.views import UserRegistrationView, UserLoginView, UserLogoutView, UserActivationView

app_name = 'accounts'

urlpatterns = [
    path('accounts/register/', UserRegistrationView.as_view(), name='register'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/activate/<uidb64>/<token>', UserActivationView.as_view(), name='activation'),
]
