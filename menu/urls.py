from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('menu-builder/', views.menu_builder, name="menu-builder"),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name="fooditems-by-category"),
    path('add-category/', views.add_category, name="add-category"),
    path('edit-category/<int:pk>/', views.edit_category, name="edit-category"),
    path('delete-category/<int:pk>/', views.delete_category, name="delete-category"),
    path('add-food/', views.add_food, name="add-food"),
]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)