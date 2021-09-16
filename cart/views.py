from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart,CartItem
from products.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

def _cartid(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request,product_id):
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(cart_product=product,user=request.user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(cart_product=product,user=request.user)
            for item in cart_item:
                item.cart_quantity+=1
                item.save()
        else:
            cart_item = CartItem.objects.create(
                cart_product  = product,
                cart_quantity = 1,
                user          = request.user,
            )
            cart_item.save()
    # If user is not logged in or authenticated.
    else:
        try:
            cart = Cart.objects.get(cart_id=_cartid(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cartid(request)
            )
            cart.save()
        is_cart_item_exists = CartItem.objects.filter(cart_product=product,cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(cart_product=product,cart=cart)
            for item in cart_item:
                item.cart_quantity+=1
                item.save()
        else:
            cart_item = CartItem.objects.create(
                cart_product  = product,
                cart_quantity = 1,
                user          = request.user,
            )
            cart_item.save()
        
    return redirect('cart')

def cart(request,total=0,quantity=0,cart_items=None):
    tax=0
    grand_total=0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cartid(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.cart_product.product_price * cart_item.cart_quantity)
            quantity += cart_item.cart_quantity
        
        tax = 75
        grand_total = total+tax
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
    }

    return render(request,'cart.html',context)

def one_cart_item_remove(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(cart_product=product,user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cartid(request))
            cart_item = CartItem.objects.get(cart_product=product,cart=cart)
        if cart_item.cart_quantity > 1 :
            cart_item.cart_quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')
    except:
        pass

def remove_from_cart(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(cart_product=product,user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cartid(request))
        cart_item = CartItem.objects.get(cart_product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')
    

@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None): 
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cartid(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.cart_product.product_price * cart_item.cart_quantity)
            quantity += cart_item.cart_quantity
        
        shipping = 75
        grand_total = total+shipping
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'shipping' : shipping,
        'grand_total' : grand_total,
    }
    return render(request,'orders/checkout.html',context)
