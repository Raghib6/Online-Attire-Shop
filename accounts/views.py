from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from products.models import Category, Product
from accounts.models import UserAccount
from accounts.forms import UserRegistrationForm
from django.contrib import messages,auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

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
            message = render_to_string('activation.html',{
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
    return render(request,'registration.html',context)

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

def passwordLength(request):
    if request.method=="GET":
        pwd = request.GET["password1"]
        if len(pwd)<8:
            return HttpResponse('Less')
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
    return render(request,'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out")
    return redirect('login')