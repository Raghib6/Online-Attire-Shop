from django.urls import path
from cart import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_to_cart/<int:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('remove_one_cart_item/<int:product_id>/',views.one_cart_item_remove,name='remove_one_cart_item'),
    path('remove_from_cart/<int:product_id>/',views.remove_from_cart,name='remove_from_cart'),

]
