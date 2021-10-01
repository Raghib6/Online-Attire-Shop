from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import UserAccount, UserProfile
from django.utils.html import format_html

class AdminAccount(UserAdmin):
    list_display = ('username','first_name','last_name','email','date_joined','last_login','is_active')
    list_filter = ('is_superuser','is_admin','is_staff','email','username','first_name')
    list_display_links = ('username','email','first_name','last_name')
    readonly_fields = ('date_joined','last_login')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    fieldsets = ()

class AdminUserProfile(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_pic.url))
    thumbnail.short_description = "Profile Picture"
    list_display = ('thumbnail','user','region','country')

admin.site.register(UserAccount,AdminAccount)
admin.site.register(UserProfile,AdminUserProfile)