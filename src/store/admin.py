from django.contrib import admin

# Register your models here.
from store.models import Category, Products, ProductVariations


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name','category','price', 'promotion_price','stock','is_available',)
    list_editable = ('price', 'stock', 'is_available', 'promotion_price',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductVariations)
class ProductVariationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'category', 'value', 'is_active')
    list_editable = ('value', 'is_active', 'category')
    list_filter = ('product', 'category', 'is_active')

