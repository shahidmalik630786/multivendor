from django.shortcuts import redirect, render, HttpResponse
from vendor.models import Vendor, UserProfile
from rest_framework.renderers import JSONRenderer
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  
from marketplace.models import FoodItem
from django.db.models import Q
from .serializers import VendorSerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from django.contrib.gis.db.models.functions import Distance


def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    context = {'vendors':vendors}
    return render(request, 'master/index.html', context)


@api_view(['GET'])
# @renderer_classes([JSONRenderer]) 
def search(request):
    rest_name = request.query_params.get('rest_name')
    latitude = request.query_params.get('latitude')
    longitude = request.query_params.get('longitude')
    radius = request.query_params.get('radius')

    vendors = Vendor.objects.none()

    if rest_name:
        fetch_vendor_by_fooditems = FoodItem.objects.filter(
            food_title__icontains=rest_name,
            is_available=True
        ).values_list('vendor', flat=True)

        vendors = Vendor.objects.filter(
            Q(id__in=fetch_vendor_by_fooditems) | Q(restaurant_name__icontains=rest_name),
            is_approved=True,
        )

        print(fetch_vendor_by_fooditems, "*************", vendors)

    if latitude and longitude and radius:
        try:
            pnt = GEOSGeometry(f'POINT({longitude} {latitude})', srid=4326)
            print(pnt, "**pnt**")
            vendors = vendors.filter(user_profile__location__distance_lte=(pnt, D(km=float(radius.replace('km', '')))))
            print(vendors, "***vendors***")
        except Exception as e:
            return Response({'error': 'Invalid coordinates or radius'}, status=400)

    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search(request):
    rest_name = request.query_params.get('rest_name')
    latitude = request.query_params.get('latitude')
    longitude = request.query_params.get('longitude')
    radius = int(request.query_params.get('radius', 5))

    # vendors = Vendor.objects.select_related('user', 'user_profile').filter(is_approved=True)

    # if rest_name:
    fetch_vendor_by_fooditems = FoodItem.objects.filter(
            food_title__icontains=rest_name,
            is_available=True
        ).values_list('vendor', flat=True)

    vendors = Vendor.objects.filter(
            Q(id__in=fetch_vendor_by_fooditems) | Q(restaurant_name__icontains=rest_name), is_approved=True, user__is_active=True
        )

    if latitude and longitude:
        try:
            user_lat = float(latitude)
            user_lng = float(longitude)
            pnt = GEOSGeometry(f'POINT({user_lng} {user_lat})', srid=4326)

            vendors = vendors.annotate(
                distance=Distance('user_profile__location', pnt)
            ).filter(
                distance__lte=D(km=radius)
            ).order_by('distance')

        except (ValueError, TypeError) as e:
            return Response({
                'error': 'Invalid location data',
                'details': str(e)
            }, status=400)
        

    serializer = VendorSerializer(vendors, many=True)
    return Response({
        'search_location': {
            'latitude': latitude,
            'longitude': longitude,
            'radius_km': radius
        },
        'count': len(serializer.data),
        'vendors': serializer.data
    })
