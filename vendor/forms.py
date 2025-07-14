from django import forms
from .models import Vendor
from vendor.models import UserProfile
from django.core.validators import MinLengthValidator, MaxLengthValidator


class VendorProfileForm(forms.ModelForm):
    pincode = forms.CharField(
        required=True,  
        validators=[MaxLengthValidator(6)],
    )
    address = forms.CharField(
        required=True,  
        validators=[MaxLengthValidator(250)],
        widget=forms.TextInput(attrs={
            'placeholder': 'start typing...', 
            'required': 'required', 
            'id': 'id_address'
        })
    )
    country = forms.CharField(
        required=True,  
        validators=[MaxLengthValidator(15)],
    )    
    state = forms.CharField(
        required=True,  
        validators=[MaxLengthValidator(15)],
    )    
    city = forms.CharField(
        required=True,  
        validators=[MaxLengthValidator(15)],
    )
    latitude = forms.CharField(
        required=True,  
        validators=[MaxLengthValidator(20)],  # Increased for decimal coordinates
        widget=forms.TextInput(attrs={'id': 'id_latitude'})
    )
    longitude = forms.CharField(
        required=True,  
        validators=[MaxLengthValidator(20)],  # Increased for decimal coordinates
        widget=forms.TextInput(attrs={'id': 'id_longitude'})
    )

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_picture', 'address', 'country', 
                 'state', 'city', 'pincode', 'latitude', 'longitude']



class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['restaurant_name', 'vendor_license']
        
