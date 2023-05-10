from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.vendor_registration, name='vendor_register'),
    path('login/', views.vendor_login, name='vendor_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/vendor/login'), name='vendor_logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('vendor_profile/', views.vendor_profile, name='vendor_profile'),

    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),

]
