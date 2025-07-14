from vendor.models import Vendor
from django.conf import settings


def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor=None
    return {"vendor": vendor}

def google_api_key(request):
    return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}