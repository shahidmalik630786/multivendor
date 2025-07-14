from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    
    path('', views.my_profile, name='my-profile'),
    path('register-user/', views.register_user, name='register-user'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('customer-dashboard/', views.customer_dashboard, name='customer-dashboard'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor-dashboard'),
    path('my-profile/', views.my_profile, name='my-profile'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('email-verification/', TemplateView.as_view(template_name='accounts/user-confirmation.html'), name='email-verification'),
    path('forget-password/', views.forgot_password, name='forget-password'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='reset-password-validate'),
    path('link-expire/', TemplateView.as_view(template_name='link-expire.html'), name='link-expire'),
    path('api/get-address/', views.get_address, name='get-address'),

    path('vendor/', include('vendor.urls'), name='vendor')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)