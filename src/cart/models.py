from django.db import models

# Create your models here.
from accounts.models import CustomUser
from store.models import Products


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Utilisateur', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Panier de {self.user}"
    
    class Meta:
        verbose_name = 'Panier'


class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Produit',)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Panier', related_name='items')
    quantity = models.IntegerField(verbose_name='Quantité', default=1)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Produits du {self.cart}"
    
    @property
    def sub_total(self):
        return self.product.promotion_price * self.quantity
    
    class Meta:
        verbose_name = 'Elément du panier'
        verbose_name_plural = 'Eléments du panier'
