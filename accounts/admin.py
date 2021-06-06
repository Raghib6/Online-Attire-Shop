from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import UserAccount


class AdminAccount(UserAdmin):
    list_display = ('username','first_name','last_name','email','date_joined','last_login','is_active')
    list_filter = ('email','username','first_name')
    list_display_links = ('username','email','first_name','last_name')
    readonly_fields = ('date_joined','last_login')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    fieldsets = ()

admin.site.register(UserAccount,AdminAccount)