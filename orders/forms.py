from django import forms


class CartItemQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput())


class DiscountTicketForm(forms.Form):
    code = forms.CharField(label="Code", widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    def clean_code(self):
        if not self.code:
            return True
        return False
