from django.urls import path
from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.registration,name='register'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('emailchecker/',views.emailChecker,name='emailchecker'),
    path('usernamechecker/',views.usernameChecker,name='usernamechecker'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('editprofile/',views.edit_profile,name='editprofile'),
    
    # Password reset
    path('password_reset/', 
    auth_views.PasswordResetView.as_view(template_name='accounts/p_reset.html'), name ='password_reset'),

    path('password_reset_done/',
    auth_views.PasswordResetDoneView.as_view(template_name='accounts/p_reset_done.html'), name ='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='accounts/p_reset_confirm.html'), name ='password_reset_confirm'),
    
    path('password_reset_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='accounts/p_reset_complete.html'), name ='password_reset_complete'),
    
    # Password change
    path('password_change/',views.change_password,name='password_change'),
    
]
