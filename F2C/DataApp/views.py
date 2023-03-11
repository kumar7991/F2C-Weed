
import json
from .constants import PaymentStatus
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views import View
from . models import CustomerProfile, Product, Cart, OrderPlaced, User
from .forms import CustomerRegistrationForm, CustomerProfileForm, FarmerRegistrationForm, ProductForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import JsonResponse


from django.shortcuts import render
from .models import Order
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
import time


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# from django.contrib.auth.decorators import user_passes_test

# def is_dashboard_user(user):
#     return user.is_authenticated and user.is_farmer
def customerlogin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                passw = form.cleaned_data['password']
                user = authenticate(username=name, password=passw )
                if user.is_customer:
                    login(request, user)
                    messages.success(request, ' logged in successfully')

                    return HttpResponseRedirect('/')
                
        else:
            form = AuthenticationForm()
        return render(request, 'app/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/')


def cust_logout(request):
    logout(request)
    return HttpResponseRedirect('/custlogin/')


class ProductView(View):
    def get(self, request):
        totalitem = 0
        Vegitable = Product.objects.filter(category='V')
        Fruits = Product.objects.filter(category='F')
        Fish = Product.objects.filter(category='Fi')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'Vegitable': Vegitable, 'Fruits': Fruits, 'Fish': Fish, 'totalitem': totalitem})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart})

import time


def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_customer:
            product_id = request.GET.get('prod-id')
            product = Product.objects.get(id=product_id)
            Cart(user=user, product=product).save()
            return redirect('/cart')
        else:
             return redirect('/cust_logout')
        
    else:
        form = AuthenticationForm()
        return render(request, 'app/login.html', {'fm': form})
    # else:
    #     time.sleep(5)
    #     return HttpResponseRedirect('/cust_logout/')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_customer:
            cart = Cart.objects.filter(user=user)
            # print(cart)
            amount = 0.0
            shipping_amount = 40
            # total_amount=0.0
            cart_product = [p for p in Cart.objects.all() if p.user == user]
        else:
            return redirect('auth_views.LoginView')
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantiry * p.product.discountd_price)
            amount += tempamount
            totalamount = amount+shipping_amount
        return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount})
    else:
        return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantiry += 1
        c.save()
        amount = 0.0
        shipping_amount = 40
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantiry * p.product.discountd_price)
            amount += tempamount

        data = {
            'quantiry': c.quantiry,
            'amount': amount,
            'totalamount': amount+shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantiry -= 1
        c.save()
        amount = 0.0
        shipping_amount = 40
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantiry * p.product.discountd_price)
            amount += tempamount

        data = {
            'quantiry': c.quantiry,
            'amount': amount,
            'totalamount': amount+shipping_amount
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 40
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantiry * p.product.discountd_price)
            amount += tempamount

        data = {
            'amount': amount,
            'totalamount': amount+shipping_amount
        }
        return JsonResponse(data)



def buy_now(request):
    if request.user.is_authenticated:
        if request.user.is_customer:
                return render(request, 'app/buynow.html')
        else:
            return redirect('/cust_logout')
    else:
        form = AuthenticationForm()
        return render(request, 'app/login.html', {'fm': form})
# def profile(request):
#  return render(request, 'app/profile.html')


@login_required
def address(request):
    user =request.user
    if user.is_customer:
        add = CustomerProfile.objects.filter(user=user)
        return render(request, 'app/address.html', {'add': add})
    else:
        return redirect('/cust_logout')

@login_required
def orders(request):
    user =request.user
    if user.is_customer:
        op = OrderPlaced.objects.filter(user=user)
        return render(request, 'app/orders.html', {'order_placed': op})
    else:
        return redirect('/cust_logout')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form= CustomerRegistrationForm(request.POST)
        if form.is_valid():
            s = form.save()
            s.is_customer = True
            s.save()
            messages.success(request, 'Registation Successfull')           
        return render(request, 'app/customerregistration.html', {'form': form})


@login_required
def checkout(request):
    user = request.user
    if user.is_customer:
        add = CustomerProfile.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 40
        totalamount = 0.0
        shipping_amount = 40
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantiry * p.product.discountd_price)
                amount += tempamount
            totalamount = amount+shipping_amount
        return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_items': cart_items})
    else:
        return redirect('/cust_logout')




@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        if request.user.is_customer:
            form = CustomerProfileForm()
            return render(request, 'app/profile.html', {'form': form,})
        else:
            return redirect('/cust_logout')
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            reg = CustomerProfile(user=usr, name=name, locality=locality,
                           city=city, state=state, pincode=pincode)
            reg.save()
            messages.success(request, 'Profile updated successfully')
        return render(request, 'app/profile.html', {'form': form})
    

def search(request):
    query=request.GET['search']
    product=Product.objects.filter(Q(title=query))
    return render(request,'app/search.html',locals())


# Farmer module

# -------------------------------------------------------------------------------------------------------------------------------------
# from django.contrib.auth.decorators import user_passes_test

# def is_dashboard_user(user):
#     return user.is_authenticated and user.is_farmer



class farmerRegistration(View):
    def get(self, request):
        form = FarmerRegistrationForm()
        return render(request, 'farmer/signup.html', {'form': form})

    def post(self, request):
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            t = form.save()
            t.is_farmer = True
            t.save()
          
            messages.success(request, 'Registation Successfull')    
        return render(request, 'farmer/signup.html', {'form': form})

def custandfarmregister(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                passw = form.cleaned_data['password']
                user = authenticate(username=name, password=passw )
                if user.is_customer:
                    login(request, user)
                    time.sleep(5)
                    s = user
                    s.is_farmer = True                  
                    s.save()
                    messages.success(request, ' logged in successfully as farmer also')

                    return redirect('farmerhome')
                
        else:
            form = AuthenticationForm()
        return render(request, 'app/login.html', {'form': form})
    else:
        return redirect('farmerhome')



def farmerlogin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                passw = form.cleaned_data['password']
                user = authenticate(username=name, password=passw )
                if user.is_farmer:
                    login(request, user)
                    messages.success(request, ' logged in successfully')

                    return redirect('farmerhome')
                
        else:
            form = AuthenticationForm()
        return render(request, 'farmer/login.html', {'fm': form})
    else:
        return redirect('farmerhome')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/flogin/')


def sellerHome(request):
    try:
     usr = request.user
     if usr.is_customer and usr.is_farmer:
         return render(request, 'farmer/sellerHome.html')
     elif usr.is_customer:
         return redirect('user_logout')
    except:
        return render(request, 'farmer/sellerHome.html')


def farmerhome(request):
    if not request.user.is_authenticated:
        form = AuthenticationForm()
        return render(request, 'farmer/login.html', {'fm': form})
    else:
        usr = request.user
        if usr.is_farmer:
            data = Product.objects.filter(user=usr)
            return render(request, 'farmer/home.html', {'data': data})
        else:
            return redirect('user_logout')

def addproducts(request):
    if not request.user.is_authenticated:
      form = AuthenticationForm()
      return render(request, 'farmer/login.html', {'fm': form})
    else:
      usr = request.user
      if usr.is_farmer:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                usr = request.user
                title = form.cleaned_data['title']
                selling_price= form.cleaned_data['selling_price']
                discountd_price = form.cleaned_data['discountd_price']
                description = form.cleaned_data['description']
                category = form.cleaned_data['category']
                quantity = form.cleaned_data['quantity']
                product_image = form.cleaned_data['product_image']
                s = Product(user=usr,title=title, selling_price=selling_price, discountd_price=discountd_price, description=description, category=category, quantity =quantity,  product_image=product_image)
                    

                s.save()
                print('created')
                return redirect('farmerhome')
            else:
                print(form.errors)
                return render(request, 'farmer/addproducts.html', {"form": form.errors})
        else:
            form = ProductForm()
      else:
          return redirect('user_logout')
          
      return render(request, 'farmer/addproducts.html', {"form": form})

    
def orderdproducts(request):
    if not request.user.is_authenticated:
      form = AuthenticationForm()
      return render(request, 'farmer/login.html', {'fm': form})
    else:
        usr = request.user
        if usr.is_farmer:
            products = OrderPlaced.objects.filter(user = usr, status = 'Accepted')
            return render(request,'farmer/orders.html', {'products':products})
        else:
          return redirect('user_logout')
def dispatched(request,id):
    if request.method == 'GET':
       numb = OrderPlaced.objects.get(pk = id)
       print(numb)
       numb.status = 'On the way' 
       numb.save()
       return HttpResponseRedirect('/custorders/')
    
def all_orders(request):
   if not request.user.is_authenticated:
      form = AuthenticationForm()
      return render(request, 'farmer/login.html', {'fm': form})
   else:
      usr = request.user
      if usr.is_farmer:
            data = OrderPlaced.objects.filter(user=usr)
            return render(request, 'farmer/allorders.html', {'data': data})
      else:
          return redirect('user_logout') 
def update_data(request, id):
    if request.method == 'POST':
        pi = Product.objects.get(pk=id)
        fm = ProductForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = Product.objects.get(pk=id)
        fm = ProductForm(instance=pi)
    return render(request, 'farmer/update.html', {'data':fm})
    



def delete_data(request, id):
    if request.method == 'POST':
        pi = Product.objects.get(pk=id)
        pi.delete()
    return HttpResponseRedirect('/')



# Payment

#-----------------------------------------------------------------------------------------------------------------------------
@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = CustomerProfile.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantiry=c.quantiry).save()
        c.delete()
    return render(request, "payment/status.html")

from django.shortcuts import render
from .models import Order
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
# from paymentIntegration.settings import (
#     RAZOR_KEY_ID,
#     RAZOR_KEY_SECRET,
# )

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

from .constants import PaymentStatus
from django.views.decorators.csrf import csrf_exempt
import json


def pay(request,totalamount):
    return render(request, "payment/index.html", {'tamount':totalamount})


def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": eval(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return render(
            request,
            "payment/payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
                "razorpay_key": settings.RAZOR_KEY_ID,
                "order": order,
            },
        )
    return render(request, "payment/payment.html")


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "payment/status.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.SUCCESS
            order.save()
            return HttpResponseRedirect('/paymentdone/')
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "payment/status.html", context={"status": order.status})




             #  FEEDBACK

# def feedback_view(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'app/feedbacksuccess.html')
#     else:
#         form = FeedbackForm()
#     return render(request, 'app/feedback.html', {'form': form})












































# from django.shortcuts import render

# # Create your views here.
# In Django, you can restrict access to a dashboard to a particular user or group of users by using the user_passes_test decorator. This decorator allows you to define a custom test function that determines whether a user is allowed to access the view.

# Here's an example of how to restrict access to a dashboard to a particular user:

# Define a custom test function in views.py:
# python
# Copy code
# from django.contrib.auth.decorators import user_passes_test

# def is_dashboard_user(user):
#     return user.is_authenticated and user.username == 'dashboarduser'
# This function checks if the user is authenticated and if their username matches the desired username (in this example, 'dashboarduser'). You can modify the condition to suit your needs.

# Use the user_passes_test decorator to restrict access to the dashboard view:
# python
# Copy code
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('dashboard/', user_passes_test(is_dashboard_user)(views.dashboard), name='dashboard'),
# ]
# Here, user_passes_test is used to restrict access to the dashboard view. The decorator takes the is_dashboard_user function as an argument, which is called to determine whether the user is allowed to access the view. If the function returns False, the user is redirected to the login page.

# Define the view function in views.py:
# python
# Copy code
# def dashboard(request):
#     # your view code here
# That's it! Now only the user with the specified username will be able to access the dashboard view. If a user with a different username tries to access the view, they will be redirected to the login page.

# Note that this method assumes that you are using Django's built-in authentication system and that you have already created the dashboarduser account.



