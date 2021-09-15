from django.http.response import JsonResponse
from django.shortcuts import render
from products.models import Category, Product
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
import json
from accounts.models import UserAccount

def home(request):
    imen = Product.objects.filter(product_cat__cat_parent__cat_name='Men')[:12]
    iwomen = Product.objects.filter(product_cat__cat_parent__cat_name='Women')[:12]
    
    if 'term' in request.GET:
        qs = Product.objects.filter(product_name__icontains=request.GET.get('term'))
        titles = []
        for product in qs:
            titles.append(product.product_name)
        return JsonResponse(titles, safe=False)

    context = {'imen':imen,'iwomen':iwomen,}
    return render(request,'index.html',context)
    
def storepage(request,category_slug=None):
    categories = None
    store_products = None

    if category_slug != None:
        if category_slug=='men' or category_slug=='Men':
            store_products = Product.objects.filter(product_cat__cat_parent__cat_name='Men')
        elif category_slug=='women' or category_slug=='Women':
            store_products = Product.objects.filter(product_cat__cat_parent__cat_name='Women')
        else:
            categories = get_object_or_404(Category,cat_slug=category_slug)
            store_products  = Product.objects.filter(product_cat = categories,is_available=True)
            print(store_products)
        paginator      = Paginator(store_products,20)
        page_numb = request.GET.get('page')
        page_products = paginator.get_page(page_numb)
        total_products = store_products.count()

    else:
        store_products = Product.objects.all().filter(is_available=True).order_by('product_name')
        paginator      = Paginator(store_products,20)
        page_numb      = request.GET.get('page')
        page_products  = paginator.get_page(page_numb)
        total_products = store_products.count()
    
    
    context = {
        'store_products' : page_products,
        'total_products' : total_products,
    }

    return render(request,'store.html',context)

def product_details(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(product_cat__cat_slug=category_slug,product_slug=product_slug)

    except Exception as e:
        raise e

    context = {
        'single_product':single_product,
    }

    return render(request,'product_details.html',context)


