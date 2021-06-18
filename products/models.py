from django.db import models
from django.db import models
from django.urls import reverse

class Category(models.Model):
    cat_name        = models.CharField(max_length=50,unique=True)
    cat_slug        = models.SlugField(max_length=150,unique=True)
    cat_parent      = models.ForeignKey("self",on_delete=models.CASCADE, null=True, blank=True,related_name="child")
    cat_image       = models.ImageField(upload_to='categories',blank=True)
    cat_created     = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # def get_url(self):
    #     return reverse('category',args=[self.cat_slug])

    def __str__(self):
        return self.cat_name


class Product(models.Model):
    product_name    = models.CharField(max_length=150)
    product_slug    = models.SlugField(max_length=200,unique=True)
    product_desc    = models.TextField(blank=True)
    product_price   = models.IntegerField()
    product_image   = models.ImageField(upload_to='products')
    product_stock   = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    product_cat     = models.ForeignKey(Category,on_delete=models.CASCADE)
    date_created    = models.DateTimeField(auto_now_add=True)
    date_modified   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    # def get_url(self):
    #     return reverse('product_details',args=[self.product_cat.cat_slug,self.product_slug])
