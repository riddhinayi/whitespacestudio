from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
import razorpay
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

# Create your views here.

def checksession(request):
    uid = request.session.get('log_id')

    if not uid:
        return None

    try:
        userdata = Login.objects.get(id=uid)
        is_seller = userdata.role == "Seller"

        if is_seller:
            try:
                profile = SellerProfile.objects.get(user=userdata)
            except SellerProfile.DoesNotExist:
                profile = None
        else:
            try:
                profile = UserProfile.objects.get(user=userdata)
            except UserProfile.DoesNotExist:
                profile = None

        context = {
            'userdata': userdata,
            'is_seller': is_seller,
            'profile': profile,
        }
        return context
    except Login.DoesNotExist:
        return None

def index(request):
    context = checksession(request)
    if context is None:
        context = {}
    allproducts = Product.objects.all()
    context['allproducts'] = allproducts
    return render(request,'index.html', context)

def about(request):
    context = checksession(request)
    return render(request,'about.html', context)

def contact1(request):
    context = checksession(request)
    if request.method == "POST":
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Subject = request.POST.get('subject')
        Message = request.POST.get('message')

        if Contact_detail.objects.filter(email=Email).exists():
            messages.error(request, 'You have already filled out contact details.')
            return redirect('contact1')  # Assuming you have a URL pattern named 'contact1'
        else:
            contactdata = Contact_detail(name=Name, email=Email, subject=Subject, message=Message)
            contactdata.save()
            messages.success(request, 'Your contact details have been saved.')
            return redirect('index')  # Ensure 'index' is the name of your URL pattern or view function

    return render(request,'contact-us.html', context)

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name1')
        email = request.POST.get('email1')
        password = request.POST.get('password1')
        phone = request.POST.get('phone1')
        role = request.POST.get('usertype')

        # Create a new Login object
        new_user = Login(name=name, email=email, password=password, phone=phone, role=role)

        # Check if role is Seller and if id_proof1 exists in request.FILES
        if role == 'Seller' and 'id_proof1' in request.FILES:
            id_proof = request.FILES['id_proof1']
            new_user.id_proof = id_proof
            messages.info(request, 'Registration done successfully. Please wait for your profile approval. It will take around 2-3 days.')
        else:
            messages.success(request, 'Data inserted successfully. You can login now.')

        new_user.save()

        # Redirect to a success page
        return redirect('index')

    return render(request, 'page-signup.html')

def login(request):
    if request.method == "POST":
        Email1 = request.POST['email2']
        Password1 = request.POST['password2']
        try:
            user = Login.objects.get(email=Email1, password=Password1)

        except Login.DoesNotExist:
            user = None

        if user is not None:
            if user.role == "Seller" and user.status == "0":
                print(user.role)
                print(user.status)
                messages.error(request, 'Your Profile is Under Approval Process. This may take upto 3 working days.')
            else:
                request.session['log_id'] = user.id
                request.session.save()
                messages.success(request, 'Login successful...')
                return redirect('/')
        else:
            messages.error(request, 'Invalid Email Id and Password. Please try again.')
            return redirect('/login')
    return render(request, 'page-login.html')

def logout(request):
    try:
        del request.session['log_id']
        messages.success(request,'your logout successfully.')
    except:
        pass
    return render(request,'index.html')

def forgotpassword(request):
    if request.method == 'POST':
        username = request.POST.get('email2')
        try:
            user = Login.objects.get(email=username)

        except Login.DoesNotExist:
            user = None
        # if user exist then only below condition will run otherwise it will give error as described in else condition.
        if user is not None:
            #################### Password Generation ##########################
            import random

            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            print(password_list)
            random.shuffle(password_list)
            print(password_list)

            password = ""  # we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################

            print(password)
            print(username)

            msg = "hello here it is your new password  " + password  # this variable will be passed as message in mail

            ############ code for sending mail ########################

            from django.core.mail import send_mail

            send_mail(
                'Your New Password',
                msg,
                'rahulinfolabz@gmail.com',
                [username],
                fail_silently=False,
            )
            # NOTE: must include below details in settings.py
            # detail tutorial - https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
            # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            # EMAIL_HOST = 'smtp.gmail.com'
            # EMAIL_USE_TLS = True
            # EMAIL_PORT = 587
            # EMAIL_HOST_USER = 'mail from which email will be sent'
            # EMAIL_HOST_PASSWORD = 'pjobvjckluqrtpkl'   #turn on 2 step verification and then generate app password which will be 16 digit code and past it here

            #############################################

            # now update the password in model
            cuser = Login.objects.get(email=username)
            cuser.password = password
            cuser.save(update_fields=['password'])

            print('Mail sent')
            messages.info(request, 'mail is sent')
            return redirect(index)

        else:
            messages.info(request, 'This account does not exist')
        return redirect(index)


def adduser(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        Address = request.POST.get('address')
        Profile_image = request.FILES.get('profile_image')
        Dob = request.POST.get('date_of_birth')
        Gender = request.POST.get('gender')

        userdata = UserProfile(user=Login(id=uid), address=Address,userprofile_image=Profile_image,date_of_birth=Dob, gender=Gender)
        userdata.save()
        messages.success(request, 'your profile data is saved.')
        return redirect(index)
    return render(request,'adduserprofile.html', context)

def showuser(request):
    context = checksession(request)
    uid = request.session['log_id']
    alluserdetails = UserProfile.objects.get(user=Login(id=uid))
    context.update({
        'alldetail': alluserdetails,
    })
    return render(request,'showuser.html', context)

def editprofile(request):
    context = checksession(request)
    uid = request.session['log_id']
    edituser = UserProfile.objects.get(user=Login(id=uid))
    context.update({
        'data': edituser,
    })
    return render(request,'edituserdetail.html',context)

def update(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        Address = request.POST.get('address1')
        Dob = request.POST.get('date_of_birth1')
        Gender = request.POST.get('gender1')
        object = UserProfile.objects.get(user=uid)
        object.address=Address
        object.date_of_birth=Dob
        object.gender=Gender

        if 'images1' in request.FILES:
            file = request.FILES['images1']
            object.userprofile_image = file
        object.save()
        messages.success(request, 'your profile has been completed..')

        return redirect('/showuser')
    return render(request,'edituserdetail.html',context)

def addseller(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        Address = request.POST.get('address')
        Profile_image = request.FILES.get('sellerprofile_image')
        Shopname = request.POST.get('shop_name')
        Shopaddress = request.POST.get('shop_address')
        yoe = request.POST.get('years_of_experience')
        spec = request.POST.get('specialization')
        ratings = request.POST.get('ratings')
        items = request.POST.get('items')
        Availibility = request.POST.get('availability')

        userdata = SellerProfile(user=Login(id=uid), address=Address, sellerprofile_image=Profile_image, shop_name=Shopname, shop_address=Shopaddress, years_of_experience=yoe, specialization=spec, rating=ratings,availability=Availibility)
        userdata.save()
        messages.success(request, 'your profile data is saved.')
        return redirect(index)
    return render(request,'addsellerprofile.html', context)

def showseller(request):
    context = checksession(request)
    uid = request.session['log_id']
    allsellerdetails = SellerProfile.objects.get(user=Login(id=uid))
    context.update({
        'sellerdetail': allsellerdetails,
    })
    return render(request,'showseller.html', context)

def editsellerdetail(request):
    context = checksession(request)
    uid = request.session['log_id']
    editseller = SellerProfile.objects.get(user=Login(id=uid))
    context.update({
        'data': editseller,
    })
    return render(request,'editsellerdetail.html',context)

def updateseller(request):
    context = checksession(request)
    uid = request.session['log_id']
    if request.method == "POST":
        Address = request.POST.get('address2')
        shop = request.POST.get('shop_name2')
        saddress = request.POST.get('shop_address2')
        yearofexp = request.POST.get('years_of_experience2')
        speci = request.POST.get('specialization2')
        rat = request.POST.get('ratings2')
        avail = request.POST.get('availability2')
        object = SellerProfile.objects.get(user=uid)
        object.address=Address
        object.shop_name=shop
        object.shop_address=saddress
        object.years_of_experience=yearofexp
        object.specialization=speci
        object.rating=rat
        object.availability=avail

        if 'seller1' in request.FILES:
            file = request.FILES['seller1']
            object.sellerprofile_image = file
        object.save()
        messages.success(request, 'your profile has been completed..')

        return redirect('/showseller')
    return render(request,'editsellerdetail.html',context)

def addproduct(request):
    context = checksession(request)
    profile6 = context.get("profile")
    print(profile6)

    if profile6 == None:
        messages.error(request, "please complete your profile.")
        return redirect('addseller')
    uid = request.session['log_id']
    categories = ProductCategory.objects.all()

    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        bid_end_date = request.POST.get('bid_end_date')

        # Create or update Product instance
        category = ProductCategory.objects.get(id=category_id)

        product = Product(Seller=Login(id=uid), Cate=category, name=name, desc=desc, price=price, image1=image)
        product.save()

        # Redirect or add additional logic as needed
        messages.success(request, 'product added successfully')
        return redirect('index')

    context.update({'categories': categories})
    return render(request,'addproduct.html', context)

def showproduct(request):
    context = checksession(request)

    uid = request.session['log_id']  # Assuming you have user authentication
    products = Product.objects.filter(Seller=uid)

    context.update({"allproducts": products})
    return render(request, 'showproduct.html', context)

def deleteProduct(request, eid):
    object = Product.objects.get(id=eid)
    object.delete()
    messages.success(request, "Product Deleted !")
    return redirect(index)

def products(request):
    context = checksession(request)
    if context is None:
        context = {}
    allproducts = Product.objects.all()
    context['allproducts'] = allproducts
    return render(request,'products.html', context)

def productdetails(request, product_id):
    context = checksession(request)
    product = Product.objects.get(id=product_id)
    context.update({'product': product})
    return render(request,'single_product.html', context)

def add_to_cart(request):
    uid = request.session['log_id']
    if request.method == 'POST':
        pid = request.POST.get('pid')
        pprice = request.POST.get('price')
        quantity = request.POST.get('quantity')
        print(quantity)
        total = int(pprice) * int(quantity)
        print(pid)
        print(pprice)
        print(quantity)
        print(total)

        existing_item = productCart.objects.filter(user=Login(id=uid), product=pid, Order_status=0).first()

        if existing_item:
            existing_item.Quantity += int(quantity)
            existing_item.save()
            messages.success(request, 'Your Product added in cart successfully')
        else:
            productdata = productCart(user=Login(id=uid), product=Product(id=pid), Price=total, Quantity=quantity, Order_id=0, Order_status=0, timeStamp="")
            productdata.save()
            messages.success(request, 'Your Product added in cart successfully')

        return redirect('/ecommerce-cart')
    else:
        return redirect('ecommerce', id=pid)


from django.shortcuts import render, redirect, get_object_or_404
import razorpay
from .models import productCart, Order
from django.contrib import messages

def ecommerce_cart(request):
    context = checksession(request)
    uid = request.session['log_id']  # Assuming you have user authentication
    cart_items = productCart.objects.filter(user__id=uid, Order_status=0)  # Adjust the filter criteria as needed

    for item in cart_items:
        item.total_price = item.product.price * item.Quantity

    total_price2 = sum(item.product.price * item.Quantity for item in cart_items)

    context.update({'cartdetails': cart_items, 'total_price2': total_price2})

    if request.method == 'POST':
        # Initialize Razorpay client and create an order
        client = razorpay.Client(auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f'))
        amount = int(total_price2 * 100)  # Convert to paisa
        data = {
            "amount": amount,
            "currency": "INR",
            "receipt": f"order_{uid}",
            "payment_capture": 1
        }

        try:
            razorpay_payment = client.order.create(data=data)
            razorpay_order_id = razorpay_payment['id']
            # Assuming you are saving order details in the database
            Order.objects.create(user=Login(id=uid), razorpay_order_id=razorpay_order_id, amount=total_price2)

            context.update({
                'razorpay_payment': {
                    'amount': amount,
                    'order_id': razorpay_order_id,
                    'key': "rzp_test_VQhEfe2NCXbbwI",  # Your Razorpay key
                },
            })
            return render(request, 'shop-cart.html', context)

        except razorpay.errors.BadRequestError as e:
            messages.error(request, f'BadRequestError: {str(e)}')
            return redirect('ecommerce_cart')  # Redirect on error
        except razorpay.errors.ServerError as e:
            messages.error(request, f'ServerError: {str(e)}')
            return redirect('ecommerce_cart')  # Redirect on error
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            return redirect('ecommerce_cart')  # Redirect on error

    return render(request, 'shop-cart.html', context)

def removefromcart(request, id):
    uid = request.session['log_id']
    products = productCart.objects.get(id=id, user=uid, Order_status=0)
    products.delete()
    return redirect('/ecommerce-cart')


from django.core.mail import send_mail
from django.shortcuts import render, redirect
import razorpay


def success(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],
    }

    client = razorpay.Client(
        auth=('rzp_test_VQhEfe2NCXbbwI', '2ibreCYL78DA3kjOhobCvz0f')
    )

    try:
        # Verify the payment signature
        client.utility.verify_payment_signature(params_dict)

        # Get the order based on the Razorpay order ID
        order = Order.objects.get(razorpay_order_id=response['razorpay_order_id'])

        # Update the Razorpay payment ID and signature in the order
        order.razorpay_payment_id = response['razorpay_payment_id']
        order.razorpay_signature = response['razorpay_signature']

        # Set the status to 'Paid' if payment is successful
        order.status = 'Paid'
        order.save()

        # Update the cart items' status to indicate they've been paid for
        productCart.objects.filter(user=order.user, Order_status=0).update(Order_status=1, Order_id=order.id)

        # Send a confirmation email
        subject = 'Payment Successful'
        message = f"Dear {order.user.name},\n\n" \
                  f"Your payment for Order ID {order.id} has been successfully processed. Thank you for choosing us!\n\n" \
                  f"Best regards,\nYour Team"
        sender_email = 'dpoza8125@gmail.com'  # Replace with your sender email address
        recipient_email = [order.user.email]

        send_mail(subject, message, sender_email, recipient_email, fail_silently=False)

        return render(request, 'success.html', {'status': True})

    except razorpay.errors.SignatureVerificationError:
        # Handle signature verification errors
        print("Signature verification failed.")
        return render(request, 'success.html', {'status': False})

    except Exception as e:
        # Handle other exceptions
        print(f"Error occurred: {str(e)}")
        return render(request, 'success.html', {'status': False})

def sellershoworder(request):
    context = checksession(request)
    profile6 = context.get("profile")
    print(profile6)

    if profile6 == None:
        messages.error(request, "please complete your profile.")
        return redirect('addseller')
    uid = request.session['log_id']
    sellers_products = Product.objects.filter(Seller=Login(id=uid))
    getdetails =  productCart.objects.filter(product__in = sellers_products , Order_status=1)
    context.update({
        "sellerorderdetails":getdetails
    })
    return render(request, 'sellershoworder.html', context)

def payment(request):
    context = checksession(request)
    uid = request.session['log_id']
    orderdata = Order.objects.filter(user=uid)
    context.update({'orderdetails': orderdata})
    return render(request, 'order.html', context)

def vieworder(request,id):
    context = checksession(request)
    user_id = request.session['log_id']
    order = Order.objects.get(id=id, user=user_id)
    orderid = order.id
    products = productCart.objects.filter(user=user_id, Order_id=orderid, Order_status=1)

    context.update({'orderitems': products})
    return render(request, 'vieworder.html', context)

def productfeedback(request, order_id):
    context = checksession(request)
    context.update({"order_id" : order_id})
    return render(request, 'feedback.html', context)

def storefeedback(request):
    context = checksession(request)
    user_id = request.session.get('log_id')
    if request.method == 'POST':
        ratings = request.POST.get('ratings')
        feedback_message = request.POST.get('feedback_message')
        order_id = request.POST.get('order_id')

        if Feedback.objects.filter(order_id=order_id).exists():
            messages.error(request, 'you have already filled feedback.')
            return redirect('/payment')
        else:
        # Assuming 'product' is a ForeignKey in the Feedback model pointing to Product
            feedback = Feedback.objects.create(
                user=Login(id=user_id),
                order_id=Order(id=order_id),
                ratings=ratings,
                comment=feedback_message,
            )

        messages.success(request, "feedback is submitted")
        return redirect(payment)
    return render(request, 'index.html', context)

def addtowishlist(request,awid):
    uid = request.session['log_id']

    try:
        wl = Wishlist.objects.get(product=Product(id=awid), user=Login(id=uid))
    except Wishlist.DoesNotExist:
        wl = None

    if wl is None:
        wldata = Wishlist(product=Product(id=awid), user=Login(id=uid))
        wldata.save()
        messages.success(request, 'Added to Wishlist.')
    else:
        messages.error(request,'Already added to wishlist')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def wishlists(request):
    context = checksession(request)
    uid = request.session['log_id']
    allproduct = Wishlist.objects.filter(user=Login(id=uid))
    context.update({'wishlistdata':allproduct})
    return render(request,'wishlist.html',context)

def removewish(request, rw):
    Wishlist.objects.filter(product=Product(id=rw)).delete()
    return redirect(wishlists)