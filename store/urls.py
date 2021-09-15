from django.urls import path
from store import views

urlpatterns = [
    path('',views.home,name='home'),
    path('store/',views.storepage,name='store'),
    path('<slug:category_slug>/',views.storepage,name='category'),
    path('<slug:category_slug>/<slug:product_slug>/',views.product_details,name='product_details'),
]
