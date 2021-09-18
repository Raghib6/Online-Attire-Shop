from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',include('admin_honeypot.urls',namespace='admin_honeypot')),
    path('oasadmin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('cart/',include('cart.urls')),
    path('orders/',include('orders.urls')),
    path('',include('store.urls')),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

