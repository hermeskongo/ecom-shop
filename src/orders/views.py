from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, TemplateView, UpdateView, DeleteView

from cart.models import Cart, CartItem
from orders.forms import OrderForm
from orders.models import Order, Payment, OrderProduct
from store.models import Products


def get_form_cleaned_data(param: str, form: OrderForm) -> str:
    """
        This function permit to get a value of a form_clean_data field
    """
    return form.cleaned_data[param]


class PlaceOrder(LoginRequiredMixin, TemplateView, FormView):
    login_url = reverse_lazy("accounts:login")
    form_class = OrderForm
    template_name = 'payments.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        
        last_name = get_form_cleaned_data('last_name', form)
        first_name = get_form_cleaned_data('first_name', form)
        phone_number = get_form_cleaned_data('phone_number', form)
        address = get_form_cleaned_data('address', form)
        country = get_form_cleaned_data('country', form)
        city = get_form_cleaned_data('city', form)
        quartier = get_form_cleaned_data('quartier', form)
        note = get_form_cleaned_data('note', form)
        email = form.cleaned_data['email']
        
        user = self.request.user
        if user:
            
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.all()
            total_w_tax = 0
            for item in cart_items:
                total_w_tax += (item.quantity * item.product.promotion_price)
            
            tax = (total_w_tax * 2) / 100
            total = tax + total_w_tax
            
            order_number = str(int(datetime.now().timestamp())) + str(int(user.id))
            if email != user.email:
                messages.error(self.request, "Veuillez laissez la même adresse que celle de votre compte")
                return redirect('cart:checkout')
            elif phone_number != user.phone_number:
                messages.error(self.request, "Veuillez laissez le même numéro de téléphone que celui de votre compte")
                return redirect('cart:checkout')
            else:
                order = Order.objects.create(
                    user=user,
                    first_name=first_name,
                    email=email,
                    order_number=order_number,
                    last_name=last_name,
                    phone_number=phone_number,
                    address=address,
                    country=country,
                    city=city,
                    quartier=quartier,
                    note=note,
                    total=total,
                    tax=tax
                )
                
                messages.success(self.request, "Votre commande a bien été exécuté")
                self.request.session['order_number'] = order_number
                super(PlaceOrder, self).form_valid(form)
                
                return redirect("orders:payments")


class OrderUpdate(UpdateView):
    form_class = OrderForm
    template_name = 'order_update.html'
    model = Order
    success_url = reverse_lazy('orders:payments')
    
    def get_context_data(self, *args,**kwargs):
        context = super(OrderUpdate, self).get_context_data(*args, **kwargs)
        
        cart = Cart.objects.get(user=self.request.user)
        
        items = CartItem.objects.filter(cart=cart)
        context['items'] = items
        return context
 
    def form_valid(self, form):
        phone_number = get_form_cleaned_data('phone_number', form)
        email = form.cleaned_data['email']
    
        order = self.get_object()
    
        user = self.request.user
        if user:
            if email != user.email:
                messages.error(self.request, "Veuillez laissez la même adresse e-mail que celle de votre compte")
                return redirect(reverse('orders:update', args=[order.id]))
            elif phone_number != user.phone_number:
                messages.error(self.request, "Veuillez laissez le même numéro de téléphone que celui de votre compte")
                return redirect(reverse('orders:update', args=[order.id]))
            else:
                super(OrderUpdate, self).form_valid(form)
                messages.success(self.request, "Vos informations ont bien été mises à jour")
                return redirect(self.success_url)
        else:
            messages.error(self.request, "Veuillez vous connecté pour accéder à cette page")
            return redirect("accounts:login")
        
        
class OrderCancel(View):
    def post(self, *args, **kwargs):
        order_id = self.kwargs['pk']
        order = Order.objects.get(id=order_id)
        order.delete()
        self.request.session.delete('order_number')
        messages.success(self.request, "Votre commande a bien été annulé :(, veuillez poursuivre vos achats :)")
        return redirect("cart:index")
    
    
class OrderPayments(TemplateView):
    template_name = 'payments.html'

    def get_context_data(self, *args, **kwargs):
        context = super(OrderPayments, self).get_context_data(*args, **kwargs)
        
        cart = Cart.objects.get(user=self.request.user)
        cart_items = cart.items.all()
        order_number = self.request.session.get('order_number', None)
        if order_number:
            order = Order.objects.get(order_number=order_number)
            total_w_tax = order.total - order.tax
            
            context['order'] = order
            context['last_name'] = order.last_name
            context['total'] = order.total
            context['tax'] = order.tax
            context['first_name'] = order.first_name
            context['phone_number'] = order.phone_number
            context['email'] = order.email
            context['address'] = order.address
            context['country'] = order.country
            context['city'] = order.city
            context['quartier'] = order.quartier
            context['items'] = cart_items
            context['total_w_tax'] = total_w_tax
            
        return context
    
    def post(self, *args, **kwargs):
        order_number = self.request.session.get('order_number')
        if order_number:
            order = Order.objects.get(order_number=order_number)
            
            payment_id = str(int(datetime.now().timestamp()))
            
            # Stockage de la transaction en base de données
            payment = Payment(
                user=self.request.user,
                payment_id=payment_id,
                method='paytest',
                amount=order.total,
                status=True,
            )
            payment.save()
            
            order.payment = payment
            order.status = 'Accepté'
            order.is_ordered = True
            order.save()
            messages.success(self.request, "Votre commande a été finalisé avec succès")
            
            # Déplacement des éléments du panier en OrderProduct
            
            user = self.request.user
            cart = Cart.objects.get(user=user)
            cart_items = cart.items.all()
            for item in cart_items:
                order_product = OrderProduct(
                    user=user,
                    payment=payment,
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    product_price=item.product.promotion_price,
                    is_ordered=True
                )
                order_product.save()
                order_product.variation.set(item.variations.all())
                order_product.save()
                # Réduire la quantité en stock du produit acheté
                
                product = Products.objects.get(
                    name=item.product.name,
                    created_at=item.product.created_at,
                )
                product.stock -= item.quantity
                product.save()
            
            # Suppression(Afin de vider) du panier de l'utilisateur (il sera recréé automatiquement)
            cart.delete()
            
            # Envoi d'un e-mail à l'acheteur pour lui confirmer sa commande
            
            message = render_to_string('order_email.html', {
                'user': self.request.user,
                'order_number': order_number
            })
            mail_subject = "Votre commande a bien été exécutée"
            
            send_mail(subject=mail_subject, message=message, html_message=message, from_email='elirameskongo1234@gmail.com', recipient_list=[self.request.user.email])
            
            return redirect("orders:complete")
        else:
            messages.error(self.request, "Vous n'avez pas accès à cette page")
            return redirect("cart:index")
        
   
class OrderComplete(TemplateView):
    template_name = 'order_complete.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(OrderComplete, self).get_context_data(*args, **kwargs)
        order_number = self.request.session.get('order_number', None)
        
        if order_number:
            order = Order.objects.get(order_number=order_number)
            order_products = OrderProduct.objects.filter(order=order)
            
            total = order.total
            tax = order.tax
            sub_total = (total - tax)
            
            context['order'] = order
            context['order_products'] = order_products
            context['total'] = total
            context['tax'] = tax
            context['sub_total'] = sub_total
            
            self.request.session.delete('order_number')
            
            return context
        else:
            return redirect('home')
    