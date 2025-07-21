from rest_framework import serializers
from vendor.models import Vendor, OpeningHour
from datetime import datetime
from django.db.models import Case, When, IntegerField
from django.shortcuts import get_object_or_404

class VendorSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='user_profile.profile_picture', read_only=True)
    address = serializers.CharField(source='user_profile.address', read_only=True)
    phone_no = serializers.CharField(source='user.phonenumber', read_only=True)
    distance_km = serializers.SerializerMethodField()
    opening_status = serializers.SerializerMethodField()


    class Meta:
        model = Vendor
        fields = [
            'id',
            'restaurant_name',
            'profile_picture',
            'address',
            'phone_no',
            'distance_km',
            'opening_status'
        ]

    def get_distance_km(self, obj):
        if hasattr(obj, 'distance') and obj.distance is not None:
            return round(obj.distance.km, 2)
        return None
    
    def get_opening_status(self, obj):
        vendor = get_object_or_404(Vendor, id=obj.id)
        # Get current day (0=Monday, 1=Tuesday, ..., 6=Sunday)
        current_day = datetime.now().weekday() + 1
        now = datetime.now()
        current_time = now.time()
        
        # Create a custom ordering that puts current day first
        opening_hours = OpeningHour.objects.filter(vendor=vendor).annotate(
            day_order=Case(
                When(day=current_day, then=0),
                default=1,
                output_field=IntegerField()
            )
        ).order_by('day_order', 'day', 'from_hour')

        # Default status
        status = "Closed"

        # Check if vendor is open now
        for slot in opening_hours:
            if slot.day == current_day and not slot.is_closed:
                # Convert from_hour and to_hour strings to time objects if they exist
                if slot.from_hour and slot.to_hour:
                    time_format = "%I:%M %p"
                    from_time = datetime.strptime(slot.from_hour, time_format).time()
                    to_time = datetime.strptime(slot.to_hour, time_format).time()
                    # Assuming from_hour and to_hour are in "HH:MM" format
                    
                    # Check if current time is within the opening hours
                    if from_time <= current_time <= to_time:
                        status = "Open"
                        break 
                    else:
                        status = "Closed"
        return status


