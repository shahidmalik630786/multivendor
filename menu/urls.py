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
    path('add-fooditem/<int:pk>/', views.add_fooditem, name="add-fooditem"),
    path('edit-fooditem/<int:pk>/', views.edit_fooditem, name="edit-fooditem"),
    path('delete-fooditem/<int:pk>/', views.delete_fooditem, name="delete-fooditem"),

    #opening hour crud
    path('opening-hour/', views.opening_hour, name="opening-hour"),
    path('add-opening-hour/', views.add_opening_hour, name="add-opening-hour"),
    path('edit-opening-hour/<int:pk>/', views.edit_opening_hour, name="edit-opening-hour"),
    path('delete-opening-hour/<int:pk>/', views.delete_opening_hour, name="delete-opening-hour"),

]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)