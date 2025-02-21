from  django import  forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'country', 'city','quartier', 'note' ]

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
   
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        