from django import forms
from django.forms import inlineformset_factory
from .models import Order, OrderItem
from decimal import Decimal

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['dish_name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= Decimal('0.00'):
            raise forms.ValidationError("Цена должна быть положительной.")
        return price

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=False
)