from django.contrib import admin

# Register your models here.
from store.models import Category, Products, ProductVariations, ReviewRating, ProductGallery


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'promotion_price', 'stock', 'is_available',)
    list_editable = ('price', 'stock', 'is_available', 'promotion_price',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductGalleryInline]


@admin.register(ProductVariations)
class ProductVariationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'category', 'value', 'is_active')
    list_editable = ('value', 'is_active', 'category')
    list_filter = ('product', 'category', 'is_active')


@admin.register(ReviewRating)
class ReviewRatingStars(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'product', 'user')
    ordering = ('created_at', 'updated_at')
    list_per_page = 25


admin.site.register(ProductGallery)
