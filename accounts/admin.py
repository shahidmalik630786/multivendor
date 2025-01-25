from django.contrib import admin
from .models import CustomUser, UserProfile
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserAdminForm
    list_display = ['email', 'firstname', 'lastname', 'phonenumber', 'role', ]
    ordering = ['-date_joined']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('customuser',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)