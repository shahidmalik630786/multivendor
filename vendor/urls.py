from django.urls import path, include
from . import views


urlpatterns = [
    path('register-vendor/', views.register_vendor, name='register-vendor'),
]