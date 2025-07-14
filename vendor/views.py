from django.shortcuts import render, redirect, get_object_or_404
from .forms import VendorForm, VendorProfileForm
from accounts.forms import UserRegisterForm
from accounts.models import CustomUser, UserProfile
from .models import Vendor
from vendor.models import UserProfile
from accounts.utils import send_verification_email
from django.urls import reverse
from django.contrib import messages
from accounts.views import check_is_vendor
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify
from django.db import transaction

def get_data(model, user):
    data = get_object_or_404(model, user=user)
    return data

def register_vendor(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if vendor_form.is_valid() and user_form.is_valid(): 
            try:
                with transaction.atomic():
                    # custom user creation
                    firstname = user_form.cleaned_data['firstname']
                    lastname = user_form.cleaned_data['lastname']
                    username = user_form.cleaned_data['username']
                    email = user_form.cleaned_data['email']
                    password = user_form.cleaned_data['password']
                    user = CustomUser.objects.create_user(firstname=firstname, lastname=lastname, username=username, email=email, password=password)
                    user.role = CustomUser.VENDOR
                    user.save()
                    # user profile creation
                    user_profile, _ = UserProfile.objects.get_or_create(user=user)
                    # vendor creation
                    vendor = vendor_form.save(commit=False)
                    vendor.user = user
                    vendor.restaurant_slug = slugify(vendor_form.cleaned_data['restaurant_name'])
                    vendor.user_profile = user_profile
                    vendor.save()
                    send_verification_email(request, user)
                    return redirect('/accounts/email-verification/')
            except Exception as e:
                print(str(e))
                messages.error(request, str(e))
    else:
        user_form = UserRegisterForm()
        vendor_form = VendorForm()
    context = {'userForm': user_form, 'vendorForm': vendor_form}
    return render(request ,'vendor/register-vendor.html', context)


@login_required
@user_passes_test(check_is_vendor)
def vendor_profile(request):
    profile = get_data(UserProfile, request.user)
    vendor = get_data(Vendor, request.user)
    if request.method == "POST":
        print(request.POST, "***************")
        profile_form = VendorProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect(reverse("vendor:vendor-profile"))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = VendorProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    
    context = {
        "vendor_form": vendor_form,
        "profile_form": profile_form,
        "profile": profile,
        "vendor": vendor
    }
    return render(request, "vendor/vendor_profile.html", context)