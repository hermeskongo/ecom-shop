from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import request, Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView

from accounts.forms import UserRegistrationForm, UserLoginForm
from accounts.models import CustomUser
from ecommerce import settings


class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('store:index')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        email = form.cleaned_data['email']
        user.save()
        
        login(self.request, user)
        
        super(UserRegistrationView, self).form_valid(form)
        
        self.send_activation_email(user)
        
        return redirect(reverse('accounts:login') + f'?command=verification&email='+email)
        
    def send_activation_email(self, user):
        token = default_token_generator.make_token(user=user)
        uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
        
        domain = get_current_site(self.request).domain
        mail_subject = "Activation de votre compte"
        activation_link = f"http://{domain}{reverse('accounts:activation', kwargs={'uidb64': uid, 'token': token})}"
        
        message = render_to_string('email_validation.html', {
            'user': user,
            'activation_link': activation_link
        })
        
        send_mail(subject=mail_subject, message=message,html_message=message, from_email='elirameskongo1234@gmail.com', recipient_list=[user.email])
        

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Vous avez bien été connecté')
        return super().form_valid(form)

    
class UserLogoutView(LogoutView):
    def dispatch(self, *args, **kwargs):
        messages.success(self.request, f"{self.request.user.first_name} a bien été déconnecté")
        return super(UserLogoutView, self).dispatch(*args, **kwargs)
    next_page = settings.LOGOUT_REDIRECT_URL
    
    
class UserActivationView(View):
    def get(self, *args, **kwargs):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = CustomUser.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(self.request, 'Félicitations, votre compte a bien été vérifié.')
            return redirect('home')
        else:
            messages.error(self.request, "Le lien d'activation est invalide ou a expiré")
            return redirect('accounts:register')
        
        