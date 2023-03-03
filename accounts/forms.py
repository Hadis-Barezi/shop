from django import forms
from . import models
from django.core.exceptions import ValidationError


class ShopUserRegisterationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)

    class Meta:
        model = models.ShopUser
        fields = ('f_name', 'l_name', 'email', 'phone', 'date_of_birth', 'image', 'password')
        widgets = {
            'f_name': forms.TextInput(attrs={'class': 'form-control'}),
            'l_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
                   }

    def clean_confirm_password(self):
        """
        password and confirm password validation

        """
        cd = self.cleaned_data
        if cd['password'] and cd['confirm_password'] and cd['password'] != cd['confirm_password']:
            raise ValidationError('Confirmation password should be equal to password.')
        return cd['confirm_password']

    def save(self, commit=True):
        """
        hash password using set_password method
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ShopUserLoginForm(forms.Form):
    phone = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
