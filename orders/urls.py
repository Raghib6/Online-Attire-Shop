from django.urls import path
from orders import views

urlpatterns = [
   path('place_order/',views.place_orders,name='place_order'),
   path('payments/',views.payments,name='payments'),
   path('order_completed/',views.order_completed,name='order_completed'),
]
