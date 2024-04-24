from django import forms
from .models import Order

# slide 48
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','address',
                  'postal_code','city']
