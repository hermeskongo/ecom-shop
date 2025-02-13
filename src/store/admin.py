from django.contrib import admin

# Register your models here.
from store.models import Category, Products


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name','category','price', 'promotion_price','stock','is_available',)
    list_editable = ('price', 'stock', 'is_available', 'promotion_price',)
    prepopulated_fields = {'slug': ('name',)}
