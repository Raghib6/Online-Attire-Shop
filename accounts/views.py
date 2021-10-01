from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from accounts.models import UserAccount, UserProfile
from accounts.forms import UserRegistrationForm,UserAccForm,UserProfileForm
from django.contrib import messages,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from orders.models import Order, ProductOrdered

# To activate user account we have to import this.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def registration(request):
    if request.method=="POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            user = UserAccount.objects.create_user(
                first_name = first_name,
                last_name  = last_name,
                email      = email,
                username   = username,
                password   = password,
            )
            user.phone = phone
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Use this to activate your account in Oshop"
            message = render_to_string('accounts/activation.html',{
                'user':user,
                'domain':current_site,
                'uid'   : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = UserRegistrationForm()
            
    context = {'form':form,}
    return render(request,'accounts/registration.html',context)

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserAccount._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,UserAccount.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulations! Your account is now verified')
        return redirect('login')

    else:
        messages.error(request,'Account is not valid')
        return redirect('registration')

def emailChecker(request):
    if request.method=="GET":
        e = request.GET["em"]
        check = UserAccount.objects.filter(email=e)
        if len(check)==1:
            return HttpResponse('Exists')
        else:
            return HttpResponse('Does not exists')

def usernameChecker(request):
    if request.method=="GET":
        usern = request.GET["uname"]
        check = UserAccount.objects.filter(username=usern)
        if len(check)==1:
            return HttpResponse('Exists')
        else:
            return HttpResponse('Does not exists')


def login(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are now logged in")
            return redirect('/')
        else:
            messages.error(request,"Invalid Login credential")
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out")
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    user_profile = get_object_or_404(UserProfile,user_id=request.user.id)
    return render(request,'accounts/profile.html',{'userprofile':user_profile})

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile,user=request.user)
    if request.method == "POST":
        user_form     = UserAccForm(request.POST,instance=request.user)
        profile_form  = UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Profile has been updated")
            return redirect('editprofile')
    else:
        user_form       = UserAccForm(instance=request.user)
        profile_form    = UserProfileForm(instance=userprofile)

    context = {
        'userprofile' : userprofile,
        'user_form'    : user_form,
        'profile_form' : profile_form,
    }
    return render(request,'accounts/edit_profile.html',context)

@login_required(login_url='login')
def change_password(request):
    if request.method=="POST":
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        user = UserAccount.objects.get(username__exact=request.user.username)

        if new_password1 == new_password2:
            check = user.check_password(old_password)
            if check:
                user.set_password(new_password1)
                user.save()
                auth.logout(request)
                messages.success(request,"Password updated successfully")
                return redirect('login')
    
            else:
                messages.error(request,"The old password you have entered is incorrect")
                return redirect('password_change')

    return render(request,'accounts/change_password.html')
    
@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-date_created')
    user_all_order = request.user.order_set.all()
    total_orders = user_all_order.filter(is_ordered=True).count()
    delivered = user_all_order.filter(status='Completed').count()
    pending = user_all_order.filter(status='Accepted').count()
    context = {'orders':orders,'user_all_order':user_all_order,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'orders/my_orders.html',context)

@login_required(login_url='login')
def order_details(request,orderid):
    order_details = ProductOrdered.objects.filter(order__order_number=orderid)
    order        = Order.objects.get(order_number=orderid)
    sub_total = 0
    for item in order_details:
        sub_total += item.product_price * item.quantity

    context = {
        'order_details' : order_details,
        'order'         : order,
        'sub_total'     : sub_total,
    }
    return render(request,'orders/order_details.html',context)