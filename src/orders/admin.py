from django.contrib import admin

# Register your models here.
from orders.models import Order, Payment, OrderProduct


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'address', 'phone_number', 'country', 'city', 'created_at', 'order_number')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'method', 'amount', 'status', 'created_at')
    

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'product_price', 'is_ordered')
    