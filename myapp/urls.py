from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact1', views.contact1, name='contact1'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('adduser', views.adduser, name='adduser'),
    path('showuser', views.showuser, name='showuser'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('update', views.update, name='update'),
    path('addseller', views.addseller, name='addseller'),
    path('showseller', views.showseller, name='showseller'),
    path('editsellerdetail', views.editsellerdetail, name='editsellerdetail'),
    path('updateseller', views.updateseller, name='updateseller'),
    path('addproduct', views.addproduct, name='addproduct'),
    path('showproduct', views.showproduct, name='showproduct'),
    path('deleteProduct/<int:eid>', views.deleteProduct, name='deleteservice'),
    path('products', views.products, name='products'),
    path('ecommerce-single/<int:product_id>/', views.productdetails, name='ecommerce-single'),
    path('ecommerce-cart', views.ecommerce_cart, name='ecommerce_cart'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('removefromcart/<int:id>', views.removefromcart, name='removefromcart'),
    path('payment-status/', views.success, name='payment_status'),
    path('sellershoworder', views.sellershoworder, name='sellershoworder'),
    path('payment', views.payment, name='payment'),
    path('vieworder/<int:id>', views.vieworder, name='vieworder'),
    path('storefeedback', views.storefeedback, name='storefeedback'),
    path('productfeedback/<int:order_id>', views.productfeedback, name='productfeedback'),
    path("addtowishlist/<int:awid>", views.addtowishlist, name="addtowishlist"),
    path("removewish/<int:rw>", views.removewish, name="removewish"),
    path('wishlist', views.wishlists, name='wishlist'),


]