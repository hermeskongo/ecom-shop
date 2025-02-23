from django.db import models

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import CustomUser
from store.models import Products, ProductVariations
from utils.constants import PAYMENT_METHODS, STATUS, COUNTRY_CHOICES, CITIES_CHOICES


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    method = models.CharField(choices=PAYMENT_METHODS, verbose_name='Méthodes de paiements', max_length=100)
    amount = models.FloatField(verbose_name='Montant')
    status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    
    def __str__(self):
        return self.payment_id
    
    class Meta:
        verbose_name = 'Paiement'


class Order(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE)
    payment = models.ForeignKey(Payment, models.SET_NULL, null=True)
    order_number = models.CharField(max_length=600, unique=True, verbose_name='Numéro de la commande')
    status = models.CharField(choices=STATUS, default='Nouveau', max_length=25)
    first_name = models.CharField(max_length=155, verbose_name='Prénom', blank=False, null=False)
    last_name = models.CharField(max_length=155, verbose_name='Nom', blank=False, null=False)
    email = models.EmailField(max_length=255, verbose_name='E-mail', blank=False, null=False)
    phone_number = PhoneNumberField(null=False, blank=False, error_messages={
        'invalid': 'Veuillez entrez un numéro de téléphone valide',
    })
    address = models.CharField(max_length=300, verbose_name='Adresse')
    country = models.CharField(choices=COUNTRY_CHOICES, verbose_name='Pays', max_length=75)
    city = models.CharField(choices=CITIES_CHOICES, verbose_name='Villes', max_length=75)
    quartier = models.CharField(max_length=100, blank=True)
    total = models.FloatField(null=False, blank=False)
    tax = models.FloatField(verbose_name='Taxe')
    note = models.TextField(verbose_name='Note pour la commande', max_length=250, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Date de modification')
    
    def __str__(self):
        return f"Commande de {self.user.first_name}"
    
    def full_name(self):
        return f"{self.first_name} {str(self.last_name).upper()}"
    
    class Meta:
        verbose_name = 'Commande'


class OrderProduct(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=False, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=False)
    variation = models.ManyToManyField(ProductVariations,blank=False, related_name='order_products_variations')
    quantity = models.IntegerField(verbose_name='Quantité')
    product_price = models.FloatField(verbose_name='Prix du produit')
    is_ordered = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.name
