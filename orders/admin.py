from django.contrib import admin
from orders.models import Payment,Order,ProductOrdered


class ProductOrderedInline(admin.TabularInline):
    model = ProductOrdered
    readonly_fields = ('user','quantity','payment','product','product_price','ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display    = ['full_name','order_number','phone','email','order_total','status','is_ordered','date_created']
    list_filter     = ['is_ordered','status']
    search_fields   = ['order_number','phone','email','first_name']
    list_per_page   = 50
    inlines = [ProductOrderedInline]
admin.site.register(Order,OrderAdmin)

admin.site.register(Payment)

admin.site.register(ProductOrdered)