from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('marketplace/', views.marketplace, name='marketplace-listing'),
    path('marketplace/<slug:vendor_slug>/', views.vendor_detail, name='vendor-detail'),
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add-to-cart'),
    path('dec-to-cart/<int:food_id>/', views.dec_to_cart, name='dec-to-cart'),
    path('total-cart-count/', views.total_cart_count, name='total-cart-count'),
    path('get-cart/', views.get_cart, name='get-cart'),
    path('get-cart-amount/', views.get_cart_amount, name='get-cart-amount'),
    path('search/<str:rest_name>/<str:location>/', views.search, name='search'),
    path('search-result/<str:food_name>/<str:location>/', views.search_result, name='search-result')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)