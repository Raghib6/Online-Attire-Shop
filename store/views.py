from orders.models import ProductOrdered
from store.forms import ReviewRatingForm
from store.models import ReviewRating
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from products.models import Category, Product
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
import json
from accounts.models import UserAccount
from django.contrib import messages
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, message
from django.conf import settings

def home(request):
    imen = Product.objects.filter(product_cat__cat_parent__cat_name='Men')[:8]
    iwomen = Product.objects.filter(product_cat__cat_parent__cat_name='Women')[:8]
    products = Product.objects.all().filter(is_available=True)
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id,status=True)
    if 'term' in request.GET:
        qs = Product.objects.filter(product_name__icontains=request.GET.get('term'))
        titles = []
        for product in qs:
            titles.append(product.product_name)
        return JsonResponse(titles, safe=False)

    context = {'imen':imen,'iwomen':iwomen,'reviews':reviews}
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
        paginator      = Paginator(store_products,9)
        page_numb = request.GET.get('page')
        page_products = paginator.get_page(page_numb)
        total_products = store_products.count()

    else:
        store_products = Product.objects.all().filter(is_available=True).order_by('product_name')
        paginator      = Paginator(store_products,9)
        page_numb      = request.GET.get('page')
        page_products  = paginator.get_page(page_numb)
        total_products = store_products.count()
    
    if 'term' in request.GET:
        qs = Product.objects.filter(product_name__icontains=request.GET.get('term'))
        titles = []
        for product in qs:
            titles.append(product.product_name)
        return JsonResponse(titles, safe=False)
    
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
    if request.user.is_authenticated:
        try:
            ordered_product = ProductOrdered.objects.filter(user=request.user,product_id=single_product.id).exists()
        except ProductOrdered.DoesNotExist:
            ordered_product = None
    else:
        ordered_product = None

    reviews = ReviewRating.objects.filter(product_id=single_product.id,status=True)
    context = {
        'single_product'  : single_product,
        'ordered_product' : ordered_product,
        'reviews'         : reviews,
    }

    return render(request,'product_details.html',context)


def submit_review(request,productid):
    current_url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id,product__id=productid)
            form = ReviewRatingForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,"Thank you! Your review has been updated")
            return redirect(current_url)
        except ReviewRating.DoesNotExist:
            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject    = form.cleaned_data['subject']
                data.rating     = form.cleaned_data['rating']
                data.review     = form.cleaned_data['review']
                data.ip         = request.META.get('REMOTE_ADDR')
                data.product_id = productid
                data.user_id    = request.user.id
                data.save()
                messages.success(request,"Thank you for your review")
                return redirect(current_url)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            store_products = Product.objects.filter(Q(product_desc__icontains=keyword) | Q(product_name__icontains=keyword))
            total_products = store_products.count()
        else:
            return render(request,'store.html',{'total_products':0})
    context = {
        'store_products' : store_products,
        'total_products' : total_products,
        'keyword'        : keyword,
    }
    return render(request,'store.html',context)


def contact(request):
    if request.method=="POST":
        message = request.POST['message']
        email   = request.POST['email']
        full_name   = request.POST['full-name']
        mail_subject = "Contact Us"
        message = render_to_string('contact.html',{
        'user'  : request.user,
        'message' : message,
        'email' : email,
        'full_name' : full_name,
    })
        to_email = 'raghibshahriar8@gmail.com'
        send_email = EmailMessage(mail_subject,message,to=[to_email])
        send_email.send()
        messages.success(request,'Email successfully sent to the admin')
    return redirect('/')