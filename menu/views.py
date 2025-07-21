from django.shortcuts import render, get_object_or_404, redirect
from vendor.models import Vendor, OpeningHour
from menu.models import Category, FoodItem
from django.contrib.auth.decorators import user_passes_test, login_required
from accounts.views import check_is_vendor
from .forms import CategoryForm, FoodItemForm, OpeningHourForm
from django.urls import reverse
from vendor.views import get_data
from django.template.defaultfilters import slugify
from django.contrib import messages

# Create your views here.
@login_required
@user_passes_test(check_is_vendor)
def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    category = Category.objects.filter(vendor=vendor).order_by('created_at')
    context ={
        "vendor": vendor,
        "category": category
    }
    return render(request, 'vendor/menu-builder.html', context)

@login_required
@user_passes_test(check_is_vendor)
def fooditems_by_category(request, pk=None):
    vendor = Vendor.objects.get(user=request.user)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    context ={
        "vendor":vendor,
        "fooditems": fooditems,
        "category": category
    }
    return render(request, "vendor/fooditems_by_category.html", context)

@login_required
@user_passes_test(check_is_vendor)
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
                category = form.save(commit=False)  
                category.vendor = get_data(Vendor, request.user) 
                category.save()  
                category.slug = slugify(category.category_name) + '-' + str(category.id)
                category.save()
                return redirect(reverse('menu:menu-builder'))
    context = {'form': form}
    return render(request, 'vendor/add_category.html', context)

@login_required
@user_passes_test(check_is_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(instance=category)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = get_data(Vendor, request.user)
            category.slug = slugify(category.category_name)
            form.save()
            return redirect(reverse("menu:menu-builder"))
    else:
        context={"form":form,
                 "category":category
                 }
        return render(request, "vendor/edit_category.html", context)

@login_required
@user_passes_test(check_is_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect(reverse("menu:menu-builder"))

@login_required
@user_passes_test(check_is_vendor)
def add_fooditem(request,pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            fooditem = form.save(commit=False)
            fooditem.vendor = get_data(Vendor, request.user)
            fooditem.category = category
            fooditem.slug = slugify(fooditem.food_title)
            fooditem.is_available=True
            fooditem.save()
            return redirect(reverse('menu:menu-builder'))
    form = FoodItemForm()
    context = {'form':form, "category":category}
    return render(request, "vendor/add_food.html", context)

@login_required
@user_passes_test(check_is_vendor)
def edit_fooditem(request, pk=None):
    fooditem = get_object_or_404(FoodItem, pk=pk)
    form = FoodItemForm(instance=fooditem)
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, instance=fooditem)
        if form.is_valid():
            fooditem = form.save(commit=False)
            fooditem.vendor = get_data(Vendor, request.user)
            fooditem.slug = slugify(fooditem.food_title)
            form.save()
            return redirect(reverse("menu:menu-builder"))
    else:
        context={"form":form,
                 "fooditem":fooditem
                 }
        return render(request, "vendor/edit-fooditem.html", context)

@login_required
@user_passes_test(check_is_vendor)
def delete_fooditem(request, pk=None):
    fooditem = get_object_or_404(FoodItem, pk=pk)
    fooditem.delete()
    return redirect(reverse("menu:menu-builder"))        

@login_required
@user_passes_test(check_is_vendor)
def opening_hour(request):
    vendor = Vendor.objects.get(user=request.user.id)
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', 'from_hour')
    context = {
        "opening_hours": opening_hours,
    }
    return render(request, "vendor/opening_hour.html", context)

@login_required
@user_passes_test(check_is_vendor)
def add_opening_hour(request):
    if request.method == 'POST':
        form = OpeningHourForm(request.POST)
        if form.is_valid():
            opening_hour = form.save(commit=False)
            opening_hour.vendor = get_data(Vendor, request.user)
            opening_hour.save()
            return redirect(reverse('menu:opening-hour'))
    else:
        form = OpeningHourForm()

    context = {'form': form}
    return render(request, 'vendor/add_opening_hour.html', context)

@login_required
@user_passes_test(check_is_vendor)
def edit_opening_hour(request, pk=None):
    opening_hour = get_object_or_404(OpeningHour, pk=pk)
    
    if request.method == "POST":
        form = OpeningHourForm(request.POST, instance=opening_hour)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.vendor = get_data(Vendor, request.user)
            instance.save()
            return redirect(reverse("menu:opening-hour"))
    else:
        form = OpeningHourForm(instance=opening_hour)

    context = {
        "form": form,
        "opening_hour": opening_hour
    }
    return render(request, "vendor/edit_opening_hour.html", context)


@login_required
@user_passes_test(check_is_vendor)
def delete_opening_hour(request, pk=None):
    category = get_object_or_404(OpeningHour, pk=pk)
    category.delete()
    return redirect(reverse("menu:opening-hour"))
