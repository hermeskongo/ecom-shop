from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
# Create your views here.
from django.views.generic import ListView, DetailView, FormView

from cart.models import Cart, CartItem
from orders.models import OrderProduct
from store.forms import ReviewRatingForm
from store.models import Products, Category, ReviewRating


class ProductsList(ListView):
    context_object_name = 'products'
    template_name = 'store.html'
    model = Products
    paginate_by = 6
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_slug = self.kwargs.get('slug', None)
        keyword = self.request.GET.get('keyword')
        
        if category_slug:
            number = self.model.objects.filter(is_available=True, category__slug=category_slug).count()
            context['number'] = number
        elif keyword:
            number = self.model.objects.filter(Q(description__icontains=keyword) | Q(name__icontains=keyword)).count()
            context['number'] = number
        else:
            context['number'] = self.model.objects.filter(is_available=True).count()
        
        return context
    
    def get_queryset(self):
        category_slug = self.kwargs.get('slug', None)
        keyword = self.request.GET.get('keyword')
        
        # Récupération de tous les produits appartenant à une certaines catégories
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            return Products.objects.filter(is_available=True, category=category).order_by('-created_at')
        
        # Moteur de recherche
        elif keyword:
            return Products.objects.filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
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
        except:
            pass
        
        try:
            bought = OrderProduct.objects.filter(product=self.get_object(), user=self.request.user).exists()
        except:
            bought = None
            
        try:
            rated = ReviewRating.objects.filter(user=self.request.user, product=self.get_object()).exists()
        except:
            rated = None
            
        reviews = ReviewRating.objects.filter(product=self.get_object()).order_by('-updated_at')
        
        context['is_added'] = is_added
        context['bought'] = bought
        context['form'] = ReviewRatingForm()
        context['reviews'] = reviews
        context['rated'] = rated
        
        return context
    
    def post(self, *args, slug=None, **kwargs):
        url = self.request.META.get('HTTP_REFERER')
        
        try:
            review = ReviewRating.objects.get(user=self.request.user, product=self.get_object())
            form = ReviewRatingForm(self.request.POST, instance=review)
            form.save()
            messages.success(self.request, "Votre avis à bien été mis à jour !")
        except ReviewRating.DoesNotExist:
            form = ReviewRatingForm(self.request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                rating = form.cleaned_data['rating']
                user = self.request.user
                product = self.get_object()
                ReviewRating.objects.create(
                    subject=subject,
                    message=message,
                    rating=rating,
                    user=user,
                    product=product
                )
                messages.success(self.request, f"Merci pour votre avis !")
        return redirect(url)
