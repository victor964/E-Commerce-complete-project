from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vendor, Product

class VendorRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ('company_name', 'contact_person_name', 'email', 'phone_number', 'address')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']

