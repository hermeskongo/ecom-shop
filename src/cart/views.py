# Create your views here.
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from cart.models import Cart, CartItem
from store.models import Products


class CartAddView(View):
    
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Products, id=self.kwargs['id'])
        
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        
        cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return redirect('cart:index')


class CartDeleteView(View):
    
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Products, id=self.kwargs['id'])
        
        cart = Cart.objects.get(user=self.request.user)
        if cart:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            
            if cart_item and cart_item.quantity > 0:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                messages.error(self.request, "Vous ne pouvez pas avoir une quantité d'articles inférieur à 0")
        else:
            messages.error(self.request, "Vous n'avez pas de panier")
        
        return redirect('cart:index')


class CartIndex(TemplateView):
    template_name = 'cart.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        
        cart_items = cart.items.all()
        
        total_w_tax = 0
        for item in cart_items:
            total_w_tax += (item.quantity * item.product.promotion_price)
        
        tax = ((total_w_tax * 2) / 100)
        total = total_w_tax + tax
        context['items'] = cart_items
        context['total_w_tax'] = total_w_tax
        context['tax'] = tax
        context['total'] = total
        
        return context


class CartItemRemoveView(View):
    
    def post(self, *args, **kwargs):
        item = get_object_or_404(CartItem, id=int(self.kwargs['id']))
        if item:
            messages.success(self.request, f"Le produit {item.product.name} à bien été supprimer")
            item.delete()
            
        return redirect('cart:index')
