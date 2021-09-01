from django.urls import path
from django.urls import path
from accounts import views

urlpatterns = [
    path('register/',views.registration,name='register'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('emailchecker/',views.emailChecker,name='emailchecker'),
    path('usernamechecker/',views.usernameChecker,name='usernamechecker'),
    path('passwordlength/',views.passwordLength,name='passwordlength'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    
]
