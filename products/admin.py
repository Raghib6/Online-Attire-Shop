from django.contrib import admin
from .models import Category,Product
 
class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {'cat_slug':('cat_name',)}
    list_display        = ['cat_name','cat_parent','cat_created']

admin.site.register(Category,AdminCategory)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name','product_price','product_stock','product_cat','date_modified','is_available']
    prepopulated_fields = {'product_slug':('product_name',)}


admin.site.register(Product,ProductAdmin)