from django.db import models

# Create your models here.
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=155, blank=False, unique=True, verbose_name="Nom de la catégorie")
    slug = models.SlugField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=500)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Catégorie'


class Products(models.Model):
    name = models.CharField(max_length=155, unique=True, verbose_name='Nom du produit')
    slug = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=800, blank=True)
    price = models.IntegerField(verbose_name='Prix')
    promotion_price = models.IntegerField(verbose_name='Prix promotionel', blank=True, default=price)
    stock = models.IntegerField(verbose_name='Stock', default=0)
    is_available = models.BooleanField(verbose_name='Disponible ?')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='pictures/products', null=False, default='')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Produit'


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(category="couleur", is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(category='taille', is_active=True)


VARIATIONS_CATEGORY_CHOICES = (
    ('couleur', 'couleur'),
    ('taille', 'taille'),
)


class ProductVariations(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variations', verbose_name='Produit')
    category = models.CharField(max_length=100, choices=VARIATIONS_CATEGORY_CHOICES, verbose_name='Type de variation')
    value = models.CharField(max_length=100, verbose_name='Valeur de la variation')
    is_active = models.BooleanField(default=True, verbose_name='actif ?')
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = VariationManager()
    
    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name = 'Variation'
