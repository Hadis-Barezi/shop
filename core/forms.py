from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext as _


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    confirm_password = forms.CharField(label=_("Password Confirmation"), widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('f_name', 'l_name', 'email', 'phone', 'date_of_birth', 'image', 'is_active', 'is_admin', 'password',
                  'confirm_password')

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


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField(help_text='you can change password <a href="../password/"> here </a>')

    class Meta:
        model = models.User
        fields = ('f_name', 'l_name', 'email', 'phone', 'date_of_birth', 'image', 'is_active', 'is_admin')
