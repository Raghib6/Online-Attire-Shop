from django.db import models
from products.models import Product
from accounts.models import UserAccount

class Cart(models.Model):
    cart_id = models.CharField(max_length=50,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user          = models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=True)
    cart_product  = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart          = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    cart_quantity = models.IntegerField()
    is_active     = models.BooleanField(default=True)

    def sub_total(self):
        return self.cart_product.product_price * self.cart_quantity

    def __str__(self):
        return self.cart_product.product_name
    
