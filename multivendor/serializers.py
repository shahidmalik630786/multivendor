from rest_framework import serializers
from vendor.models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='user_profile.profile_picture', read_only=True)
    address = serializers.CharField(source='user_profile.address', read_only=True)
    phone_no = serializers.CharField(source='user.phonenumber', read_only=True)
    distance_km = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = [
            'id',
            'restaurant_name',
            'profile_picture',
            'address',
            'phone_no',
            'distance_km',
        ]

    def get_distance_km(self, obj):
        if hasattr(obj, 'distance') and obj.distance is not None:
            return round(obj.distance.km, 2)
        return None

