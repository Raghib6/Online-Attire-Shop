from accounts.models import UserAccount
from django.db import models
from accounts.models import UserAccount
import products.models

class ReviewRating(models.Model):
    product = models.ForeignKey("products.Product",on_delete=models.CASCADE)
    user    = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    subject = models.CharField(max_length=150,blank=True)
    review  = models.TextField(max_length=500,blank=True)
    rating  = models.FloatField()
    ip      = models.CharField(max_length=50,blank=True)
    status  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    