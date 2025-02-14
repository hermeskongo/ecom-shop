from django.urls import path

from cart.views import CartAddView, CartIndex, CartDeleteView, CartItemRemoveView

app_name = 'cart'

urlpatterns = [
    path('cart/', CartIndex.as_view(), name='index'),
    path('cart/add/<int:id>', CartAddView.as_view(), name='add'),
    path('cart/reduce/<int:id>', CartDeleteView.as_view(), name='reduce'),
    path('cart/remove/<int:id>', CartItemRemoveView.as_view(), name='remove'),
]
