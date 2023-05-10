from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    TITLE_CHOICES = (
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=4, choices=TITLE_CHOICES, null=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    email = models.EmailField(max_length=100, null=True)
    date_of_birth = models.DateField(null=True)
    phone_no = models.CharField(max_length=12, null=True)
    date_created =models.DateTimeField(auto_now_add=True, null=True)
