import os

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField

from utils.constants import COUNTRY_CHOICES, CITIES_CHOICES


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True, blank=True, null=True, error_messages={
        'unique':'Il existe déjà un utilisateur avec ce numéro',
        'invalid': 'Veuillez entrez un numéro de téléphone valide'
    })
    email = models.EmailField(unique=True, blank=False, null=False,
                              error_messages={'unique': 'Il existe déjà un utilisateur avec cet e-mail', })
    address = models.CharField(max_length=155, blank=False, null=False, verbose_name='Adresse')
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    MAIL_FIELD = "email"
    REQUIRED_FIELDS = ["address", "username"]
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super(CustomUser, self).save(*args, **kwargs)
  

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    country = models.CharField(max_length=50, verbose_name='Pays', choices=COUNTRY_CHOICES, blank=True,)
    city = models.CharField(max_length=50, verbose_name='Ville', choices=CITIES_CHOICES, blank=True,)
    quartier = models.CharField(max_length=70, verbose_name='Quartier', blank=True)
    picture = models.ImageField(verbose_name='Photo de profile', upload_to='profile', null=True, blank=True)
    
    def delete(self, *args, **kwargs):
        if self.picture:
            if os.path.exists(self.picture.path):
                os.remove(self.picture.path)
        return super(UserProfile, self).delete(*args, **kwargs)