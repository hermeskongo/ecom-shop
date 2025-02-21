# Create your views here.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView

from cart.models import Cart, CartItem
from orders.forms import OrderForm
from store.models import Products, ProductVariations


class CartAddView(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')
    
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Products, id=self.kwargs['id'])
        
        # Ajout des différentes variations au produits
        product_variations = []
        for item in self.request.POST:
            key = item
            value = self.request.POST.get(key)
            if key != 'csrfmiddlewaretoken':
                try:
                    variation = ProductVariations.objects.filter(category__iexact=key, value__iexact=value).first()
                    print(variation)
                    if variation:
                        product_variations.append(variation)
                except:
                    pass
        
        print(product_variations)
        
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        
        # Vérifie si l'élément existe
        cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()
        
        if cart_item_exist:
            cart_items = CartItem.objects.filter(product=product, cart=cart)
            
            exist_variations_list = []
            ids = []
            
            for item in cart_items:
                item_variations = item.variations.all()
                exist_variations_list.append(list(item_variations))
                ids.append(item.id)
            
            if product_variations in exist_variations_list:
                index = exist_variations_list.index(product_variations)
                item_id = ids[index]
                item = CartItem.objects.get(product=product, cart=cart, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, cart=cart)
                item.variations.set(product_variations)
                item.save()
        else:
            if product_variations:
                cart_item = CartItem.objects.create(product=product, cart=cart)
                cart_item.variations.set(product_variations)
                cart_item.save()
        
        return redirect('cart:index')
    
    def handle_no_permission(self):
        messages.error(self.request, "Vous devez être connecté pour effectuer cette action")
        return redirect(self.login_url)


class CartDeleteView(View):
    
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Products, id=self.kwargs['product_id'])
        item_id = self.kwargs['cart_item_id']
        
        cart = Cart.objects.get(user=self.request.user)
        if cart:
            cart_item = CartItem.objects.get(product=product, cart=cart, id=item_id)
            
            if cart_item and cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        else:
            messages.error(self.request, "Vous n'avez pas de panier")
        
        return redirect('cart:index')


class CartIndex(LoginRequiredMixin, TemplateView, FormView):
    template_name = 'cart.html'
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'next'
    form_class = OrderForm
    
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
    
    def handle_no_permission(self):
        messages.error(self.request, "Vous devez être connecté pour accéder à cette page")
        return super(CartIndex, self).handle_no_permission()
    

class CartItemRemoveView(View):
    
    def post(self, *args, **kwargs):
        item = get_object_or_404(CartItem, id=int(self.kwargs['id']))
        if item:
            product_name = item.product.name
            item.delete()
            messages.success(self.request, f"Le produit {product_name} à bien été supprimer")
        
        return redirect('cart:index')


class CheckoutView(TemplateView):
    template_name = "checkout.html"
