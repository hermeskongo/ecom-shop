from django.urls import path

from orders.views import PlaceOrder, OrderPayments, OrderComplete, OrderUpdate, OrderCancel

app_name = 'orders'

urlpatterns = [
    path('order/placeorder/', PlaceOrder.as_view(), name='placeorder'),
    path('order/payments/', OrderPayments.as_view(), name='payments'),
    path('order/update/<int:pk>', OrderUpdate.as_view(), name='update'),
    path('order/complete/', OrderComplete.as_view(), name='complete'),
    path('order/cancel/<int:pk>', OrderCancel.as_view(), name='cancel'),
]
