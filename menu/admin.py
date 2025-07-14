from django.contrib import admin
from .models import Category, FoodItem
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'vendor')
    search_fields = ('category_name', 'vendor__restaurant_name')

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('food_title',)}
    list_display = ('food_title', 'vendor', 'category', 'price', 'is_available')
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name', 'price')



admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
