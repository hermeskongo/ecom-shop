from django.urls import path

from store.views import ProductsList, ProductDetails

app_name = 'store'

urlpatterns = [
    path('store/', ProductsList.as_view(), name='index'),
    path('store/category/<slug:slug>/', ProductsList.as_view(), name='index'),
    path('store/details/<slug:slug>/', ProductDetails.as_view(), name='product-details'),
    path('store/search/', ProductsList.as_view(), name='search'),
]
