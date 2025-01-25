from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .utils import detect_user, send_verification_email, send_password_reset_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


#restrict the customer from accessing user vendor page
def check_is_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

#restrict the vendor from accessing user customer page
def check_is_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

# Create your views here.
def register_user(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in!')
        return render(request, 'index.html')
    elif request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = CustomUser.CUSTOMER
            password = form.cleaned_data['password']
            user.set_password(password)
            form.save()
            send_verification_email(request, user)
            messages.success(request, "Your account has been registered successfully")
            return redirect('/accounts/email-verification/')
        return render(request ,'accounts/register-user.html', {'form':form})
    else:
        form = UserRegisterForm()
        return render(request ,'accounts/register-user.html', {'form':form})
    
def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in!')
        return render(request, 'index.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    else:
        return render(request, 'accounts/login.html')
    messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

@user_passes_test(check_is_customer)
def customer_dashboard(request):
    return render(request, 'accounts/customer-dashboard.html')

@user_passes_test(check_is_vendor)
def vendor_dashboard(request):
    return render(request, 'accounts/vendor-dashboard.html')

@login_required
def my_profile(request):
    user = request.user
    redirectUrl = detect_user(user)
    return redirect(redirectUrl)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, CustomUser.DoesNotExist, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("/accounts/login")
    
def forgot_password(request):
    if request.method == "POST":
        email =  request.POST.get('email')
        user = CustomUser.objects.filter(email = email).first()
        if user:
            send_password_reset_email(request, user)
        else:
            messages.error(request, 'Email doesnt exit')
            return render(request, "accounts/forgot-password.html")
    return render(request, "accounts/forgot-password.html")

def reset_password(request):
    return render(request, "accounts/reset-password.html")

def reset_password_validate(request):
    return render(request, "accounts/forgot-password.html")