from django.urls import path

from orders.views import PlaceOrder, OrderPayments, OrderComplete

app_name = 'orders'

urlpatterns = [
    path('order/placeorder/', PlaceOrder.as_view(), name='placeorder'),
    path('order/payments/', OrderPayments.as_view(), name='payments'),
    path('order/complete/', OrderComplete.as_view(), name='complete'),
]
