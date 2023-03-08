from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.views import View
from . import forms
from . import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order


class ShopUserRegister(View):
    form_class = forms.ShopUserRegisterationForm
    template_name = 'accounts/register.html'
    model = models.ShopUser

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILE)
        if form.is_valid():
            cd = form.cleaned_data
            user = self.model.objects.create_user(f_name=cd['f_name'], l_name=cd['l_name'], email=cd['email'],
                                                  phone=cd['phone'], password=cd['password'])
            if cd['image']:
                user.image = cd['image']
            if cd['date_of_birth']:
                user.date_of_birth = cd['date_of_birth']
            user.save()
            messages.success(request, f"you registered successfully.", 'success')
            if self.next:
                return redirect(self.next)
            return redirect('products:home')
        return render(request, template_name=self.template_name, context={'form': form})


class ShopUserLogin(View):
    form_class = forms.ShopUserLoginForm
    template_name = "accounts/login.html"

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("products:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['phone'], password=cd['password'])
            if user:
                login(request, user)
                messages.success(request, f"you logged in successfully.", 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('products:home')
        messages.error(request, "username or password is wrong", 'warning')
        return render(request, template_name=self.template_name, context={'form': form})


class ShopUserLogout(LoginRequiredMixin, View):
    # login_url = "account:login"
    def get(self, request):
        logout(request)
        messages.success(request, f"you logged out successfully.", 'success')
        return redirect('products:home')


class ShopUserProfile(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'
    user_class = models.ShopUser

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(self.user_class, pk=kwargs['user_id'])
        self.addresses = self.user.addresses.all()
        self.orders = self.user.orders.all()
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.id == self.user.id:
            messages.error(request, f"you are not allowed", 'danger')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        return render(request, template_name=self.template_name, context={'user': self.user, 'addresses': self.addresses, 'orders': self.orders})


class EditShopUserProfile(LoginRequiredMixin, View):
    form_class = forms.ShopUserEditeForm
    user_class = models.ShopUser
    template_name = 'accounts/edit_profile.html'

    def setup(self, request, *args, **kwargs):
        self.user = get_object_or_404(self.user_class, pk=kwargs['user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.id == self.user.id:
            messages.error(request, f"you are not allowed", 'danger')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.user)
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"your profile updated successfully.", 'success')
            return redirect('accounts:profile', kwargs['user_id'])
        return render(request, template_name=self.template_name, context={'form': form})


class ChangePassword(LoginRequiredMixin, View):
    form_class = forms.ShopUserChangePasswordForm
    shop_user_class = models.ShopUser
    template_name = 'accounts/change_password.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.id == kwargs['user_id']:
            messages.error(request, f"you are not allowed", 'danger')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request, user_id):
        form = self.form_class()
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request, user_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = self.shop_user_class.objects.get(id=user_id)
            user.change_password(new_password=cd['new_password'], old_password=cd['old_password'])
            user.save()
            messages.success(request, "your password change successfully.", "success")
            return redirect("accounts:profile", user_id)
        return render(request, template_name=self.template_name, context={'form': form})


class ShopUserAddressList(LoginRequiredMixin, View):
    address_class = models.Address
    template_name = 'accounts/address_list.html'

    def get(self, request):
        addresses = self.address_class.objects.filter(shop_user=request.user.id)
        return render(request, template_name=self.template_name, context={'addresses': addresses})


class AddAddress(LoginRequiredMixin, View):
    form_class = forms.CreateUpdateAddressForm
    address_model = models.Address
    user_model = models.ShopUser
    template_name = 'accounts/new_address.html'

    def get(self, request):
        form = self.form_class()
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_address = form.save(commit=False)
            new_address.shop_user = self.user_model.objects.get(id=request.user.id)
            new_address.save()
            messages.success(request, f"A new address Added successfully.", 'success')
            return redirect('accounts:address_list')
        return render(request, template_name=self.template_name, context={'form': form})


class EditAddress(LoginRequiredMixin, View):
    form_class = forms.CreateUpdateAddressForm
    address_model = models.Address
    template_name = 'accounts/edit_address.html'

    def setup(self, request, *args, **kwargs):
        self.address = get_object_or_404(self.address_model, id=kwargs['address_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.id == self.address.shop_user.id:
            messages.error(request, f"you are not allowed", 'danger')
            return redirect('product:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.address)
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            self.address.province = cd['province']
            self. address.city = cd['city']
            self.address.street = cd['street'],
            self.address.postal_code = cd['postal_code']
            self.address.more_detail = cd['more_detail']
            self.address.save()
            messages.success(request, f"your address updated successfully.", 'success')
            return redirect('accounts:address_list')
        return render(request, template_name=self.template_name, context={'form': form})


class DeleteAddress(LoginRequiredMixin, View):
    address_model = models.Address

    def setup(self, request, *args, **kwargs):
        self.address = get_object_or_404(self.address_model, id=kwargs['address_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.id == self.address.shop_user.id:
            messages.error(request, f"you are not allowed", 'danger')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.address.delete()
        messages.success(request, f"your address deleted successfully.", 'success')
        return redirect('accounts:address_list')


class ShopUserOrderList(LoginRequiredMixin, View):
    order_model = Order
    user_model = models.ShopUser
    templates_name = 'accounts/shop_user_orders.html'

    def setup(self, request, *args, **kwargs):
        self.orders = self.order_model.objects.filter(shop_user=kwargs['shop_user_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.id == kwargs['shop_user_id']:
            messages.error(request, f"you are not allowed", 'danger')
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.templates_name, context={'orders': self.orders})



