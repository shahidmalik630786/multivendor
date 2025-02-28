from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.http import JsonResponse
from vendor.models import Vendor
from accounts.models import UserProfile
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from marketplace.models import Cart
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_is_customer
from django.db.models import Sum

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
        }
    return render(request, "marketplace/listing.html", context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, restaurant_slug=vendor_slug)
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        category = Category.objects.filter(vendor=vendor).prefetch_related(
            Prefetch(
                'fooditems',
                queryset=FoodItem.objects.filter(is_available=True)
            )
        )
        cart_dict = {}
        for item in cart_items:
            cart_dict[item.fooditem.id] = item.quantity

            
        context = {
            "vendor": vendor,
            "category": category,
            "cart_items": cart_dict
        }
    else:
        category = Category.objects.filter(vendor=vendor).prefetch_related(Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
            ))
        context={
            "vendor": vendor,
            "category": category
                }
    return render(request, "marketplace/vendor_detail.html", context)

@user_passes_test(check_is_customer)
def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if food_id:
            fooditem = get_object_or_404(FoodItem, id=food_id)
            try:
                cart, created = Cart.objects.get_or_create(user=request.user, fooditem = fooditem)
                cart.quantity+=1
                cart.save()
                return JsonResponse({'status':"success", 'message': 'cart updated successfully'})
            except Exception as e:
                return JsonResponse({'status':"Failed", 'message': str(e)})
        return JsonResponse({'status': "failed", 'message': str(e)}, status=400)
    return JsonResponse({'status': "failed", 'message': 'user not authenticated'}, status=401) 

@user_passes_test(check_is_customer)
def dec_to_cart(request, food_id):
    if request.user.is_authenticated:
        if food_id:
            fooditem = get_object_or_404(FoodItem, id=food_id)
            try:
                cart, created = Cart.objects.get_or_create(user=request.user, fooditem = fooditem)
                if cart.quantity > 0:
                    cart.quantity-=1
                    cart.save()
                if cart.quantity == 0:
                    cart.delete()
                    return JsonResponse({'status':"success", 'message': 'cart updated successfully'})
                return JsonResponse({'status':"Failed", 'message': 'cart quantity is 0'})
            except Exception as e:
                return JsonResponse({'status':"Failed", 'message': str(e)})
        return JsonResponse({'status': "failed", 'message': str(e)}, status=400)
    return JsonResponse({'status': "failed", 'message': 'user not authenticated'}, status=401) 

@user_passes_test(check_is_customer)
@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {"carts": cart}
    return render(request, "marketplace/cart.html")

def get_cart(request):
    try:
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user=request.user).order_by('modified_at')
            cart_data = [
                {
                "item_id": item.id,
                "food_id": item.fooditem.id,
                "food_title": item.fooditem.food_title,
                "food_description": item.fooditem.description,
                "food_price": item.fooditem.price,
                "quantity": item.quantity,
                "image_url": item.fooditem.image.url
                }
                for item in cart_items
            ]
            return JsonResponse({'status': "success", 'data':cart_data}, status=200)
        else:
            return JsonResponse({'status': 'failure', 'message': 'user not authenticated'}, status=401)
    except Exception as e:
        return JsonResponse({'status':'failure', "msg":str(e) })
    

@user_passes_test(check_is_customer)
def total_cart_count(request):
    try:
        cart = Cart.objects.filter(user=request.user).aggregate(Sum('quantity'))['quantity__sum']
        return JsonResponse({'status':"success", "data": cart}, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
    
def get_cart_amount(request):
    sub_total = 0
    tax = 0
    grand_total = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            sub_total = sum(item.quantity * item.fooditem.price for item in cart_items)
            grand_total= sub_total+tax
            return JsonResponse({"status": "success", "sub_total": sub_total, "tax": 0, "grand_total": grand_total}, status=200)
        except Exception as e:
            return JsonResponse({"status": "success", "error": str(e)}, status=200)
    else:
        return JsonResponse({'status': 'failure', 'message': 'user not authenticated'}, status=401)
            
def search(request, rest_name, location):
    context = {"rest_name":rest_name, "location":location}
    return render(request, "marketplace/search.html", context)

def search_result(request, food_name=None, location=None):
    food_name = None if food_name == "None" else food_name
    location = None if location == "None" else location
    print(food_name)
    if request.user.is_authenticated:
        filters={}
        if food_name:
            filters["food_title__icontains"] = food_name
            fooditem = FoodItem.objects.filter(**filters)
        elif location:
            filters["vendor__user_profile__address__icontains"] = location
            fooditem = FoodItem.objects.filter(**filters)
        else:
            fooditem = FoodItem.objects.all()
        data = [
                {
                    "restaurant_name":food.food_title,
                    "restaurant_slug":food.slug,
                    "location":food.vendor.user_profile.address,
                    "user_profile": food.image.url if food.image else "/static/assets/images/default-food.png",
                } 
                for food in fooditem
                ]
        print(data)
        return JsonResponse({"status": "success", "data": data}, status=200)
    else:
        return JsonResponse({'status': 'failure', 'message': 'user not authenticated'}, status=401)
    



