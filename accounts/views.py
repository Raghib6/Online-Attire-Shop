from django.contrib.auth.models import User
from django.shortcuts import render
from products.models import Category, Product
from accounts.forms import UserRegistrationForm

def registration(request):
    form = UserRegistrationForm()
    context = {'form':form,}
    return render(request,'registration.html',context)
