from django.contrib import admin
from .models import Category,Product
from django.utils.html import format_html

class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {'cat_slug':('cat_name',)}
    list_display        = ['cat_name','cat_parent','cat_created']
    search_fields       = ['cat_name']

admin.site.register(Category,AdminCategory)


class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="50" style="border-radius:50%;">'.format(object.product_image.url))
    thumbnail.short_description = "Profile Picture"
    list_filter     = ['product_cat','product_stock']
    search_fields   = ['product_name','product_cat']
    list_display = ['product_name','product_price','thumbnail','product_stock','product_cat','date_modified','is_available']
    prepopulated_fields = {'product_slug':('product_name',)}


admin.site.register(Product,ProductAdmin)