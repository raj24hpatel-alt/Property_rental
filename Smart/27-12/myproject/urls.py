"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('about',views.about),
    path('properties-details/<int:id>',views.property),
    path('add-properties',views.addproperty),
    path('insertproperty',views.insertproperty),
    path('removeproperties/<int:id>',views.removeproperties),
    path('editproperties/<int:id>',views.editproperties),
    path('updateproperty',views.updateproperties),
    path('manageproperties',views.manageproperties),
    path('propertiesvs1',views.propertiesvs1),
    path('propertiesvs2', views.propertiesvs2),
    path('payment_success', views.payment_success),
    path('placeorder',views.placeorder),
    path('bookinghistory',views.userbookinghistory),
    path('givefeedback',views.givefeedback),
    path('viewfeedback',views.viewfeedback),
    path('register',views.register),
    path('login',views.login,name='login'),
    path('service',views.service),
    path('single-service',views.singleservice),
    path('contact',views.contact_view),
    path('registerdata',views.Register),
    path('logindata',views.logindata),
    path('logout',views.logout),
    path('viewbookinghistory',views.sellerhistory),
    path('addwishlist/<int:id>', views.addwishlist, name='addwishlist'),
    path('wishlistpage', views.wishlistpage, name='wishlistpage'),
    path('removewishlist/<int:id>/', views.removewishlist),
    path('update-booking/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),# myapp/urls.py
    path('viewbookinghistory/', views.userbookinghistory, name='viewbookinghistory'),
    path('invoice/<int:id>/', views.invoice, name='invoice'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('delete-image/<int:id>', views.delete_image, name='delete_image'),


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

