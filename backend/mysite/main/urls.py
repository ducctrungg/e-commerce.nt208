from django.urls import path
from . import views
# this file set routing in web
urlpatterns = [
    path('',views.home, name='home'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('register/',views.registerPage, name='register'),
    path('account/',views.accountPage, name='account'),
    path('admin/',views.adminPage, name='admin'),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('products/<slug:slug>',views.productDetails, name='productDetails'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name='process_order'),

    path('create_order/',views.createOrder, name='create_order'),
    path('create_orderitem/',views.createOrderItem, name='create_orderitem'),
    path('create_product/',views.createProduct, name='create_product'),
    path('create_customer/',views.createCustomer, name='create_customer'),


    path('update_order/<str:pk>',views.updateOrder, name='update_order'),
    path('update_orderitem/<str:pk>',views.updateOrderItem, name='update_orderitem'),
    path('update_product/<str:pk>',views.updateProduct, name='update_product'),
    path('update_customer/<str:pk>',views.updateCustomer, name='update_customer'),


    path('delete_order/<str:pk>',views.deleteOrder, name='delete_order'),
    path('delete_customer/<str:pk>',views.deleteCustomer, name='delete_customer'),
    path('delete_orderitem/<str:pk>',views.deleteOrderItem, name='delete_orderitem'),
    path('delete_product/<str:pk>',views.deleteProduct, name='delete_product'),

    path('dashboard/',views.dashboardPage, name='process_order'),
]