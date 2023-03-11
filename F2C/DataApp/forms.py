from django import forms
from .models import User


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
# from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import CustomerProfile, Product

# class RegisterForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email','phone_no','is_farmer','is_customer','is_deliverer','Address','Pincode','date','date_joined']







class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='ConformPassword', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2','phone_no','is_farmer','is_active','Address','Pincode','date_joined']
        exclude = ['is_farmer','is_customer','is_deliverer','date_joined','Last login','Superuser status','Groups','User permissions','Staff status','is_active']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(
            attrs={'class': 'form-control'})}


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplate': 'curent-password', 'class': 'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplate': 'curent-password', 'autofocus': True, 'class': 'form-control'}))
    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplate': 'new-password', 'class': 'form-control'}),
                                    help_text=password_validation.
                                    password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm New Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplate': 'new-password', 'class': 'form-control'})),


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['name', 'locality', 'city', 'state', 'pincode']
        widgets = {'name': forms.TextInput(attrs={'class': "form-control"}),
                   'locality': forms.TextInput(attrs={'class': "form-control"}),
                   'city': forms.TextInput(attrs={'class': "form-control"}),
                   'state': forms.Select(attrs={'class': "form-control"}),
                   'pincode': forms.NumberInput(attrs={'class': "form-control"})
                   }


class FarmerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='ConformPassword', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2','phone_no','is_farmer','is_active','Address','Pincode','date_joined']
        exclude = ['is_farmer','is_customer','is_deliverer','date_joined','Last login','Superuser status','Groups','User permissions','Staff status','is_active']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(
            attrs={'class': 'form-control'})}

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        exclude = ['user',]