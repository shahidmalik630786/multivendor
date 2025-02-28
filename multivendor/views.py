from django.shortcuts import redirect, render, HttpResponse
from vendor.models import Vendor

def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    context = {'vendors':vendors}
    return render(request, 'master/index.html', context)