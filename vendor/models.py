from django.db import models
from accounts.models import CustomUser, UserProfile

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(CustomUser, related_name='vendor', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='vendor_profile', on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=15)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vendor"

    def __str__(self):
        return str(self.restaurant_name)
