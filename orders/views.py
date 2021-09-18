from django.shortcuts import render,redirect
from cart.models import CartItem
from orders.forms import OrderForm
from orders.models import Order,Payment,ProductOrdered
import datetime,json
from products.models import Product
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, message
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


def place_orders(request,total=0,quantity=0):
    current_user = request.user
    cart_items   = CartItem.objects.filter(user=current_user)
    cart_count   = cart_items.count()
    if cart_count <= 0:
        return redirect('/')
    grand_total = 0
    shipping      = 75
    for cart_item in cart_items:
        total += (cart_item.cart_product.product_price * cart_item.cart_quantity)
        quantity += cart_item.cart_quantity
    
    grand_total = total+shipping
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user           = current_user
            data.first_name     = form.cleaned_data['first_name']
            data.last_name      = form.cleaned_data['last_name']
            data.phone          = form.cleaned_data['phone']
            data.email          = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.upazila_thana  = form.cleaned_data['upazila_thana']
            data.city           = form.cleaned_data['city']
            data.order_note     = form.cleaned_data['order_note']
            data.shipping       = shipping
            data.order_total    = grand_total
            data.ip             = request.META.get('REMOTE_ADDR')
            data.save()

            yr                  = int(datetime.date.today().strftime('%Y'))
            dt                  = int(datetime.date.today().strftime('%d'))
            mt                  = int(datetime.date.today().strftime('%m'))
            d                   = datetime.date(yr,mt,dt)
            current_date        = d.strftime("%Y%m%d")
            order_number        = current_date + str(data.id)
            data.order_number   = order_number
            data.save()
            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context = {
                'order'       : order,
                'cart_items'  : cart_items,
                'total'       : total,
                'grand_total' : grand_total,
                'shipping'    : shipping,
            }
            return render(request,'orders/payments.html',context)
    else:
        return redirect('checkout')


def payments(request):
    body  = json.loads(request.body)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])

    payment = Payment(
        user            = request.user,
        payment_id      = body['transactionID'],
        payment_method  = body['payment_method'],
        amount_paid     = order.order_total,
        status           = body['status'],
    )
    payment.save()

    order.payment       = payment
    order.is_ordered    = True
    order.save()

    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        ordered_product = ProductOrdered()
        ordered_product.order_id = order.id
        ordered_product.payment = payment
        ordered_product.user_id = request.user.id
        ordered_product.product_id = item.cart_product_id
        ordered_product.quantity = item.cart_quantity
        ordered_product.product_price = item.cart_product.product_price
        ordered_product.ordered = True
        ordered_product.save()


        product = Product.objects.get(id=item.cart_product_id)
        product.product_stock-=item.cart_quantity
        product.save()
    CartItem.objects.filter(user=request.user).delete()

    mail_subject = "Thank you for your order in Online Attire Shop"
    message = render_to_string('orders/order_received.html',{
        'user'  : request.user,
        'order' :order
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message,to=[to_email])
    send_email.send()

    data = {
        'order_number'  : order.order_number,
        'transactionId' : payment.payment_id,
    }
    return JsonResponse(data,safe=False)


def order_completed(request):
    order_number   = request.GET.get('order_number') #order_number is from payments.html url
    transactionId = request.GET.get('payment_id') #payment_id is from payments.html url
    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products = ProductOrdered.objects.filter(order_id=order.id)
        for item in ordered_products:
            sub_total = item.product_price * item.quantity

        payment = Payment.objects.get(payment_id=transactionId)

        context = {
            'order_number' : order.order_number,
            'order' : order,
            'ordered_products' : ordered_products,
            'transactionId'  : payment.payment_id,
            'payment'        : payment,
            'sub_total'      : sub_total,
        }
        return render(request,'orders/order_completed.html',context)

    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('store')

