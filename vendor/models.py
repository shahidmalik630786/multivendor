from django.db import models
from accounts.models import CustomUser, UserProfile
from accounts.utils import send_notification
from django.core.validators import FileExtensionValidator
from datetime import time

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(CustomUser, related_name='vendor', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='vendor_profile', on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=15, unique=True)
    restaurant_slug = models.SlugField(max_length=100, blank=True, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])] )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "vendor"

    def __str__(self):
        return str(self.restaurant_name)
    
    def save(self, *args, **kwargs):
        if self.pk:
            try:
                vendor = Vendor.objects.get(pk=self.pk)
                if vendor.is_approved != self.is_approved:
                    context = {
                        'user': self.user,
                        'is_approved':self.is_approved,
                        'restaurant_name': self.restaurant_name,
                    }
                    if self.is_approved == True:
                        mail_subject = "Congragulations you are restaurant is approved"
                    else:
                        mail_subject = "we are sorry you are restaurant is not approved"
                    send_notification(mail_subject, context)
            except Vendor.DoesNotExist:
                pass
        return super().save(*args, **kwargs)


DAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]

HOUR_OF_DAY_24 = [
    (time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p'))
    for h in range(0, 24)
    for m in (0, 30)
]
class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)
    

    class Meta:
        ordering = ('day', 'from_hour')
        unique_together = ('vendor', 'day', 'from_hour', 'to_hour')


