from django import forms
from .models import Category, FoodItem

from vendor.models import OpeningHour

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'description']

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['food_title', 'description', 'price', 'image', 'is_available']


class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']