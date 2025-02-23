import os

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView, TemplateView, ListView, UpdateView, DetailView

from accounts.forms import UserRegistrationForm, UserLoginForm, ForgotPasswordForm, ResetPasswordForm, UserForm, \
    UserProfileForm
from utils.mixins import CustomLoginRequiredMixin
from accounts.models import CustomUser, UserProfile
from ecommerce import settings
from orders.models import Order, OrderProduct


class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('store:index')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        email = form.cleaned_data['email']
        user.save()
        UserProfile.objects.create(user=user)
        
        super(UserRegistrationView, self).form_valid(form)
        
        self.send_activation_email(user)
        
        return redirect(reverse('accounts:login') + f'?command=verification&email=' + email)
    
    def send_activation_email(self, user: CustomUser) -> None:
        """
        This function permit to send a validation e-mail to user
        """
        
        token = default_token_generator.make_token(user=user)
        uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
        
        domain = get_current_site(self.request).domain
        mail_subject = "Activation de votre compte"
        activation_link = f"http://{domain}{reverse('accounts:activation', kwargs={'uidb64': uid, 'token': token})}"
        
        message = render_to_string('email_validation.html', {
            'user': user,
            'activation_link': activation_link
        })
        
        send_mail(subject=mail_subject, message=message, html_message=message, from_email='elirameskongo1234@gmail.com',
                  recipient_list=[user.email])


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'
    
    def form_valid(self, form):
        messages.success(self.request, "Vous avez été connecté avec succès")
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.request.POST.get('next') or reverse_lazy('accounts:dashboard')


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
            return redirect('accounts:login')
        else:
            messages.error(self.request, "Le lien d'activation est invalide ou a expiré")
            return redirect('accounts:register')


class UserDashboardView(CustomLoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = reverse_lazy("accounts:login")
    
    def get_context_data(self, *args, **kwargs):
        context = super(UserDashboardView, self).get_context_data(*args, **kwargs)
        
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        
        order = Order.objects.filter(user=self.request.user).order_by('-created_at')
        counter_order = order.count()
        context['counter_order'] = counter_order
        context['user_profile'] = user_profile
        
        return context


class UserDashboardOrdersView(CustomLoginRequiredMixin, ListView):
    template_name = 'dashboard_orders.html'
    login_url = reverse_lazy("accounts:login")
    context_object_name = 'orders'
    model = Order
    
    def get_queryset(self, *args, **kwargs):
        related_orders = Order.objects.filter(user=self.request.user).order_by("-updated_at")
        
        return related_orders


class UserDashboardOrderDetails(DetailView):
    model = Order
    template_name = 'order_details.html'
    context_object_name = 'order'
    
    def get_context_data(self, *args,**kwargs):
        context = super(UserDashboardOrderDetails, self).get_context_data(*args, **kwargs)
        
        order = self.get_object()
        user = self.request.user
        total = order.total
        tax = order.tax
        sub_total = (order.total - order.tax)
        
        order_products = OrderProduct.objects.filter(user=user, order=order)
        
        context['order_products'] = order_products
        context['total'] = total
        context['tax'] = tax
        context['sub_total'] = sub_total
        
        return context

class UserDashboardChangeProfile(CustomLoginRequiredMixin, TemplateView):
    template_name = 'dashboard_profile.html'
    
    def post(self, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        user_form = UserForm(self.request.POST, instance=self.request.user)
        profile_form = UserProfileForm(self.request.POST, self.request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            
            if not self.request.FILES == {}:
                # Suppression de l'ancienne images en cas mise à jour de la photo de profile afin d'optimiser l'espace
                if profile_form.cleaned_data['picture'] and user_profile.picture:
                    print()
                    path = user_profile.picture.path
                    new_path = path.split('src')[0] + "src"
                    old_picture_path = new_path + str(user_profile.picture.url)
                    if os.path.exists(old_picture_path):
                        os.remove(old_picture_path)
            
            else:
                if user_profile.picture:
                    profile_form.cleaned_data['picture'] = user_profile.picture
            profile_form.save()
            messages.success(self.request, "Mise à jour réussi !")
            return redirect("accounts:dashboard_profile")
        
        return self.render_to_response(context={
            'user_form': user_form,
            'profile_form': profile_form,
            'user_profile': user_profile
        })
    
    def get_context_data(self, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        
        context = super(UserDashboardChangeProfile, self).get_context_data(*args, **kwargs)
        
        user_form = UserForm(instance=self.request.user)
        profile_form = UserProfileForm(instance=user_profile)
        
        if user_profile:
            context['user_profile'] = user_profile
        
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        
        return context


class UserDashboardChangePassword(CustomLoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'dashboard_change_password.html'
    success_url = reverse_lazy("accounts:dashboard_password")
    
    def dispatch(self, *args, **kwargs):
        if self.request.method == 'POST' and self.get_form().is_valid():
            messages.success(self.request, "Votre mot de passe a bien été modifié")
        return super(UserDashboardChangePassword, self).dispatch(*args, **kwargs)


class UserForgotPassword(FormView):
    template_name = 'forgot_password.html'
    form_class = ForgotPasswordForm
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email__exact=email)
            self.request.session['uid'] = user.id
            self.send_reset_password_email(user)
            messages.success(
                self.request,
                f"Nous vous avons envoyé un e-mail({user.email}) pour la réinitialisation de votre mot de passe."
            )
            return redirect('accounts:forgot_password')
        else:
            messages.error(
                self.request,
                "Aucun utilisateur avec cet e-mail n'existe"
            )
            return redirect('accounts:forgot_password')
    
    def send_reset_password_email(self, user):
        """
        This method permit to send a reset password email to a specific user
        """
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(str(user.id).encode('utf-8'))
        
        domain_site = get_current_site(self.request).domain
        activation_link = f"http://{domain_site}/accounts/reset_password_validate/{uidb64}/{token}"
        
        mail_subject = 'Réinitialisation de votre de passe'
        
        message = render_to_string('reset_password_email.html', {
            'user': user,
            'activation_link': activation_link,
        })
        send_mail(mail_subject, message, 'elirameskongo1234@gmail.com', [user.email], html_message=message)


class UserResetValidateView(View):
    def get(self, *args, **kwargs):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = CustomUser.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        
        if user and default_token_generator.check_token(user, token):
            self.request.session['uid'] = user.id
            messages.success(self.request, "Veuillez réinitialiser votre mot de passe")
            return redirect('accounts:reset_password')
        else:
            messages.error(self.request, "Le token est invalide ou à expirer")
            return redirect('accounts:forgot_password')


class UserResetPassword(FormView):
    template_name = 'reset_password.html'
    form_class = ResetPasswordForm
    
    def form_valid(self, form):
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']
        
        if password == confirm_password:
            uid = self.request.session.get('uid')
            if uid:
                if len(password) < 8:
                    messages.error(self.request, "Votre mot de passe doit contenir au moins 08 caractères")
                    return redirect("accounts:reset_password")
                elif password.isdigit():
                    messages.error(self.request, "Votre mot de passe ne peut contenir que des chiffres")
                    return redirect("accounts:reset_password")
                elif password.islower():
                    messages.error(self.request, "Votre mot de passe doit contenir au moins une majuscule")
                    return redirect("accounts:reset_password")
                elif password.isupper():
                    messages.error(self.request, "Votre mot de passe doit contenir au moins une minuscule")
                    return redirect("accounts:reset_password")
                elif password.isspace():
                    messages.error(self.request, "Votre mot de passe ne doit pas contenir d'espace")
                    return redirect("accounts:reset_password")
                else:
                    user = CustomUser.objects.get(id=uid)
                    user.set_password(password)
                    user.save()
                    messages.success(self.request, "Votre mot de passe à été modifié avec succès")
                    return redirect("accounts:login")
            
            else:
                messages.error(self.request, "Erreur dans le processus. Veuillez recommencer ou contacter le "
                                             "propriétaire du site")
                return redirect("accounts:forgot_password")
        else:
            messages.error(self.request, "Les mots de passe doivent correspondre")
            return redirect('accounts:reset_password')
