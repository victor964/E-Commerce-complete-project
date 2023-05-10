from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from .forms import VendorRegistrationForm, VendorForm, ProductForm
from .models import Vendor, Product

from django.contrib import messages

# Create your views here.
def vendor_registration(request):
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='Vendor')
            user.groups.add(group)

            Vendor.objects.create(user=user)

            return redirect('/vendor/login')
    else:
        form = VendorRegistrationForm()
    return render(request, 'vendor/register.html', {'form': form})


def vendor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.groups.filter(name='Vendor').exists():
                login(request, user)
                return redirect('/vendor/dashboard')
            else:
                return render(request, 'vendor/login.html', {'error_message': 'You are not a registered vendor!'})
        else:
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'vendor/login.html', {'error_message': error_message})
    else:
        return render(request, 'vendor/login.html')


def dashboard(request):
    all_products = Product.objects.all()

    context = {'products': all_products}
    return render(request, 'vendor/dashboard.html', context)


def vendor_profile(request):
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=request.user.vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('/vendor/dashboard')
    else:
        form = VendorForm(instance=request.user.vendor)
    context = {'form': form}
    return render(request, 'vendor/vendor_profile.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.save()
            return redirect('/vendor/dashboard')
    else:
        form = ProductForm()
    return render(request, 'vendor/add_product.html', {'form': form})


def edit_product(request, product_id):
    # Get the product instance from the database or show a 404 page
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Populate the form with the data from the request
        form = ProductForm(request.POST, instance=product)

        # If the form is valid, save the changes and redirect to the product list page
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('/vendor/dashboard')
    else:
        # Render the form with the current product instance data
        form = ProductForm(instance=product)

    context = {'form': form, 'product': product}
    return render(request, 'vendor/edit_product.html', context)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('/vendor/dashboard') 
    
    context = {'product': product}
    return render(request, 'vendor/delete_product.html', context)

