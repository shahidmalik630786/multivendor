from django.urls import path, include
from . import views
from accounts.views import vendor_dashboard


urlpatterns = [
    path('', vendor_dashboard),
    path('register-vendor/', views.register_vendor, name='register-vendor'),
    path('vendor-profile/', views.vendor_profile, name="vendor-profile")
]