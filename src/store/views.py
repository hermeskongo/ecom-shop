from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.generic import ListView, DetailView

from store.models import Products, Category


class ProductsList(ListView):
    context_object_name = 'products'
    template_name = 'store.html'
    model = Products
    
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
            return Products.objects.filter(is_available=True, category=category)
        return Products.objects.filter(is_available=True)


class ProductDetails(DetailView):
    model = Products
    context_object_name = 'product'
    template_name = 'product-detail.html'
