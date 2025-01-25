from django.shortcuts import render, redirect
from .forms import VendorForm
from accounts.forms import UserRegisterForm
from accounts.models import CustomUser, UserProfile
from accounts.utils import send_verification_email

def register_vendor(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if vendor_form.is_valid() and user_form.is_valid():
            firstname = user_form.cleaned_data['firstname']
            lastname = user_form.cleaned_data['lastname']
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            user = CustomUser.objects.create_user(firstname=firstname, lastname=lastname, username=username, email=email, password=password)
            user.role = CustomUser.VENDOR
            user.save()

            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile, _ = UserProfile.objects.get_or_create(user=user)
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = user_profile
            vendor.save()
            send_verification_email(request, user)
            return redirect('/accounts/email-verification/')
    else:
        user_form = UserRegisterForm()
        vendor_form = VendorForm()
    context = {'userForm': user_form, 'vendorForm': vendor_form}
    return render(request ,'vendor/register-vendor.html', context)

    