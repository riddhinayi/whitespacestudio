from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'password', 'phone', "role", "status","id_proof")
    search_fields = ('name', 'email')

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'user_image', 'date_of_birth', "gender","loyalty_points")

@admin.register(SellerProfile)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'seller_image', 'shop_name', "shop_address", "years_of_experience","specialization","rating","availability")

@admin.register(Contact_detail)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message', 'timestamp')

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['cateName']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('Seller', 'name', 'Cate', 'price', 'timestamp', 'pic')

@admin.register(productCart)
class ProductCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'Price', 'Quantity', 'Order_status', 'timeStamp')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature','status')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_id', 'ratings', 'comment', 'timestamp')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')