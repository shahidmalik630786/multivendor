from marketplace.models import Cart

def cart_product_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.filter(user=request.user).count()
        except Exception as e:
            cart=None
        return {"cart_product_count": cart}
    else:
        return {"cart_product_count": None}