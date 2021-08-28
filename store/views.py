from django.shortcuts import render
from products.models import Category, Product

def home(request):
    men = Product.objects.filter(product_cat__cat_parent__cat_name='Men')[:12]
    women = Product.objects.filter(product_cat__cat_parent__cat_name='Women')[:12]
    
    context = {'men':men,'women':women,}
    return render(request,'index.html',context)
    
def storepage(request):
    return render(request,'store.html')