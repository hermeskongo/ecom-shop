from django.shortcuts import render

from store.models import Products


def home(request):
    products = Products.objects.filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request, 'index.html', context=context)
