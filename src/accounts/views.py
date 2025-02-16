from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import request
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import FormView

from accounts.forms import UserRegistrationForm, UserLoginForm
from ecommerce import settings


class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('store:index')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        
        login(self.request, user)
        
        super(UserRegistrationView, self).form_valid(form)
        
        return redirect(self.success_url)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Vous avez bien été connecté')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL
    