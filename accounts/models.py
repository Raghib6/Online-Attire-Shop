from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager


class UserAccount(AbstractBaseUser):
    first_name      =       models.CharField(max_length=50)
    last_name       =       models.CharField(max_length=50)
    username        =       models.CharField(max_length=50,unique=True)
    email           =       models.EmailField(max_length=150,unique=True)
    phone           =       models.PositiveIntegerField(null=True)

    # required fields

    date_joined     =       models.DateTimeField(auto_now_add=True)
    last_login      =       models.DateTimeField(auto_now_add=True)
    is_superuser    =       models.BooleanField(default=False)
    is_admin        =       models.BooleanField(default=False)
    is_staff        =       models.BooleanField(default=False)
    is_active       =       models.BooleanField(default=False)

    USERNAME_FIELD  =       'email'
    REQUIRED_FIELDS =       ['username','first_name','last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True

class UserProfile(models.Model):
    user            = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    address_line1   = models.CharField(null=True,blank=True, max_length=150)
    address_line2   = models.CharField(null=True,blank=True, max_length=150)
    profile_pic     = models.ImageField(blank=True,upload_to='profile_pic')
    region          = models.CharField(blank=True,max_length=50)
    country         = models.CharField(default="Bangladesh",blank=True,max_length=50)

    def __str__(self):
        return self.user.first_name #from useraccount accessing first name

    def full_address(self):
        return f"{self.address_line1},{self.address_line2}"
    