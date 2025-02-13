from django.urls import path

from store.views import ProductsList, ProductDetails

app_name = 'store'

urlpatterns = [
    path('store/', ProductsList.as_view(), name='index'),
    path('store/<slug:slug>/', ProductsList.as_view(), name='index'),
    path('store/details/<slug:slug>', ProductDetails.as_view(), name='product-details')
]
