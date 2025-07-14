from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import FileExtensionValidator
from django.contrib.gis.geos import Point


class CustomManager(BaseUserManager):
    def create_user(self, email,  password=None, **extra_fields):
        
        if not email:
            raise ValueError('Email field cannot be empty')
        
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None, **extra_fields):
        user = self.create_user(
            email = self.normalize_email(email),
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Consumer')
    )
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phonenumber = models.CharField(max_length=12, blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    #required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomManager()

    class Meta:
        db_table = "customuser"

    def __str__(self):
        return str(self.email)
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        if self.role == 2:
            user_role = 'Consumer'
        return user_role


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='userprofile', on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])] ,blank=True, null=True)
    cover_picture = models.ImageField(upload_to='users/cover_picture', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])] ,blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    state = models.CharField(max_length=40, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.CharField(max_length=10, null=True, blank=True)
    longitude = models.CharField(max_length=10, null=True, blank=True)
    location = models.PointField(null=True, blank=True, srid=4326) 
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profile"

    def __str__(self):
        return str(self.user)
    
    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            self.location = Point(float(self.longitude), float(self.latitude))
            return super(UserProfile, self).save(*args, **kwargs)
    





