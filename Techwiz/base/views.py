import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .utils import account_activation_token

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from .forms import CustomerRegistrationForm, CustomerForm
from django.contrib import messages

from .models import Customer

# Create your views here.
def index(request):

    context = {}
    return render(request, 'base/index.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user account but don't activate it yet
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            group = Group.objects.get(name='Customer')
            user.groups.add(group)

            Customer.objects.create(user=user)

            # Send a confirmation email
            subject = 'Confirm Your Account'
            message = render_to_string('base/activation_email.html', {
                'user': user,
                'domain': request.get_host(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            text_message = strip_tags(message)

            sender_email = settings.EMAIL_HOST_USER
            receiver_email = user.email

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = receiver_email
            part1 = MIMEText(text_message, 'plain')
            part2 = MIMEText(message, 'html')
            msg.attach(part1)
            msg.attach(part2)

            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp:
                smtp.starttls()
                smtp.login(user=sender_email, password=settings.EMAIL_HOST_PASSWORD)
                smtp.sendmail(
                    from_addr=sender_email, 
                    to_addrs=receiver_email,
                    msg=msg.as_string()
                )

            return render(request, 'base/registration_success.html')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'base/register.html', {'form': form})
    

User = get_user_model()

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can <a href="/login/">login</a> to your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def login_customer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/my_account/profile')
        else:
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'base/login.html', {'error_message': error_message})
    else:
        return render(request, 'base/login.html')
    

def logout_customer(request):
    logout(request)
    return redirect('/login')
    
def accounts(request):
    customer = request.user.customer

    context = {'customer':customer}
    return render(request, 'base/account.html', context)


def user_profile(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=request.user.customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('/my_account/orders')
    else:
        form = CustomerForm(instance=request.user.customer)
    context = {'form': form}
    return render(request, 'base/profile.html', context)