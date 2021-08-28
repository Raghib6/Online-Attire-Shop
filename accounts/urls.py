from django.urls import path
from django.urls import path
from accounts import views

urlpatterns = [
    path('register/',views.registration,name='register'),
    # path('login/',views.login,name='login'),
    # path('logout/',views.logout,name='logout'),
    
]
