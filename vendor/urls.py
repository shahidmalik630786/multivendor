from django.urls import path, include
from . import views
from accounts.views import vendor_dashboard
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', vendor_dashboard),
    path('register-vendor/', views.register_vendor, name='register-vendor'),
    path('vendor-profile/', views.vendor_profile, name="vendor-profile"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)