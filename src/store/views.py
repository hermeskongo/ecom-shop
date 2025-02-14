from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.generic import ListView, DetailView

from cart.models import Cart, CartItem
from store.models import Products, Category


class ProductsList(ListView):
    context_object_name = 'products'
    template_name = 'store.html'
    model = Products
    paginate_by = 6
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_slug = self.kwargs.get('slug', None)
        if category_slug:
            number = self.model.objects.filter(is_available=True, category__slug=category_slug).count()
            context['number'] = number
        else:
            context['number'] = self.model.objects.filter(is_available=True).count()
        
        return context
    
    def get_queryset(self):
        category_slug = self.kwargs.get('slug', None)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            return Products.objects.filter(is_available=True, category=category).order_by('-created_at')
        return Products.objects.filter(is_available=True).order_by('-created_at')


class ProductDetails(DetailView):
    model = Products
    context_object_name = 'product'
    template_name = 'product-detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        is_added = False
        
        try:
            cart = Cart.objects.get(user=self.request.user)
            if cart:
                item = CartItem.objects.get(cart=cart, product=self.get_object())
                if item:
                    is_added = True
            context['is_added'] = is_added
        except :
            pass
        
        context['is_added'] = is_added
        
        return context
