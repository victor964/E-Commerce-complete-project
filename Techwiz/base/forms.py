from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    # password = forms.CharField(widget=forms.PasswordInput())
    # confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def clean(self):
    #     cleaned_data = super(CustomerRegistrationForm, self).clean()
    #     password = cleaned_data.get('password')
    #     confirm_password = cleaned_data.get('confirm_password')

    #     if password != confirm_password:
    #         raise forms.ValidationError("Passwords do not match")


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('title', 'first_name', 'last_name', 'email', 'phone_no' )