from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.registerPage, name='register'),
    path('account/',views.accountPage, name='account'),
    path('admin/',views.adminPage, name='admin'),
    path('cart/',views.cart, name='cart'),
    path('cart_test/',views.cartTest, name='cart_test'),
    path('checkout/',views.checkout, name='checkout'),
    path('products/<slug:slug>',views.productDetails, name='productDetails'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name='process_order'),
]