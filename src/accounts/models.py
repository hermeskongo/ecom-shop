from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField


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
        