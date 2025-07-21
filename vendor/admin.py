from django.contrib import admin
from .models import Vendor, OpeningHour
# Register your models here.

class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor',"day", "from_hour", "to_hour")  

admin.site.register(Vendor)
admin.site.register(OpeningHour, OpeningHourAdmin)
