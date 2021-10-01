from django.contrib import admin
from store.models import ReviewRating
from products.models import Product
from accounts.models import UserAccount

class AdminRating(admin.ModelAdmin):
    list_filter         = ('rating','status','user__email','product__product_name')
    search_fields       = ['product__product_name','user__email']
    list_display        = ['product','category','user','rating','status','updated_at']

    @staticmethod
    def category(self):
        return self.product.product_cat

admin.site.register(ReviewRating,AdminRating)
