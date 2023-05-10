from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),

    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='customer_activate'),
    path('login/', views.login_customer, name='customer_login'),
    path('logout/', views.logout_customer, name='logout'),

    path('my_account/orders', views.accounts, name='my_account'),
    path('my_account/profile', views.user_profile, name='profile'),

]