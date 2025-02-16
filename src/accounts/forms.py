from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        
        self.set_attrs('first_name', 'placeholder', 'Entrer votre prénom')
        self.set_attrs('last_name', 'placeholder', 'Entrer votre nom')
        self.set_attrs('email', 'placeholder', 'Entrer votre email')
        self.set_attrs('phone_number', 'placeholder', 'Entrer numéro (Ex: +226 72529678)')
        self.set_attrs('phone_number', 'required', True)
        self.set_attrs('address', 'placeholder', 'Entrer votre adresse')
        self.set_attrs('password1', 'placeholder', 'Mot de passe')
        self.set_attrs('password2', 'placeholder', 'Répéter votre mot de passe')
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    def set_attrs(self, field_name: str, attribute: str, value):
        """
        This method permit to set automatically an attribute with field_name, attribute_value and value
        """
        self.fields[field_name].widget.attrs[attribute] = value


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    def set_attrs(self, field_name: str, attribute: str, value):
        """
        This method permit to set automatically an attribute with field_name, attribute_value and value
        """
        self.fields[field_name].widget.attrs[attribute] = value
