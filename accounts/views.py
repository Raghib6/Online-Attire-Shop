from django.shortcuts import render
from products.models import Product
# Create your views here.
def home(request):
    products = Product.objects.all()[:12]
    context = {'products':products}
    return render(request,'index.html',context)