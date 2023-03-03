from django import forms


class CartItemQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput())