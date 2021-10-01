from django.contrib import admin
from orders.models import Payment,Order,ProductOrdered
from products.models import Product
from accounts.models import UserAccount
from django.utils.html import format_html

class ProductOrderedInline(admin.TabularInline):
    model = ProductOrdered
    readonly_fields = ('user','quantity','payment','product','product_price','ordered')
    extra = 0

@admin.display(description='product_name')
def product_nam(obj):
    return ("%s" % (obj.product_name)).upper()

@admin.display(description='email')
def email(obj):
    return ("%s" % (obj.email))

class ProductOrderedAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="40" style="border-radius:50%;">'.format(object.product.product_image.url))
    list_filter     = ['product','user']
    search_fields   = ['order__order_number','product__product_name','user__email']
    list_display    = ['order_num','product_nam','email','thumbnail','quantity','updated_at']

    @admin.display(description='product_name')
    def product_nam(self,obj):
        return ("%s" % (obj.product.product_name))

    @admin.display(description='email')
    def email(self,obj):
        return ("%s" % (obj.user.email))

    @admin.display(description='order_number')
    def order_num(self,obj):
        return ("%s" % (obj.order.order_number))

admin.site.register(ProductOrdered,ProductOrderedAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display    = ['full_name','order_number','phone','email','order_total','status','is_ordered','date_created']
    list_filter     = ['is_ordered','status']
    search_fields   = ['order_number','phone','email','first_name']
    list_per_page   = 50
    inlines = [ProductOrderedInline]

admin.site.register(Order,OrderAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_filter     = ['user']
    search_fields   = ['user__email','payment_id']
    list_display    = ['user','payment_id','amount_paid','status','date_created']

admin.site.register(Payment,PaymentAdmin)

