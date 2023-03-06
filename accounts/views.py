from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.views import View
from . import forms
from . import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


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
        try:
            self.user = get_object_or_404(self.user_class, pk=kwargs['user_id'])
        except:
            messages.error(request, f"No user with id ={kwargs['user_id']}.", 'danger')
            return redirect("products:home")
        else:
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
        try:
            self.user = get_object_or_404(self.user_class, pk=kwargs['user_id'])
        except:
            messages.error(request, f"No user with id ={kwargs['user_id']}.", 'danger')
            return redirect("products:home")
        else:
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



