from cart.models import Cart, CartItem
from store.models import Category


def menu_links(request):
    categories = Category.objects.all()
    return dict(categories=categories)


def counter(request):
    cart_counter = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.filter(cart=cart)
            
            for item in cart_item:
                cart_counter += item.quantity
        except Cart.DoesNotExist:
            cart_counter = 0
    
    return dict(cart_counter=cart_counter)
