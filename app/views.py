from django.shortcuts import render, redirect
from django.views import View  # importing View class
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse


class ProductView(View):
    def get(self, request):
        # the given filters the products on the basis of category TW
        topwears = Product.objects.filter(category='TW')  # TW=Top wear
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        context = {'topwears': topwears,
                   'bottomwears': bottomwears, 'mobiles': mobiles}
        return render(request, 'app/home.html', context)


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'product': product})


def add_to_cart(request):
    user = request.user  # fetching current users
    # fetching product id from product_detail page
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)  # getting product instance
    Cart(user=user, product=product).save()  # saving Cart data in database
    return redirect('/cart')
    # return render(request, 'app/addtocart.html')


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        #list comprehension to store cart data of authenticated user
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount+= temp_amount
                total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart,'total_amount':total_amount,'amount':amount})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount+= temp_amount
            total_amount = amount + shipping_amount

        data = {
            'quantity':c.quantity,
            'amount' :amount,
            'totalamount':total_amount
            }
        return JsonResponse(data)

def buy_now(request):
    return render(request, 'app/buynow.html')


def address(request):
    # filtering customers on the basis of current users
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add})


def orders(request):
    return render(request, 'app/orders.html')


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung' or data == 'iPhone':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        # lt = less than, inbuilt django function
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__lt=500)
    elif data == 'above':
        # gt = greater than, inbuilt django function
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__gt=500)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})


def topwears(request):
    topwears = Product.objects.filter(category='TW')
    return render(request, 'app/topwears.html', {'topwears': topwears})


def bottomwears(request):
    bottomwears = Product.objects.filter(category='BW')
    return render(request, 'app/bottomwears.html', {'bottomwears': bottomwears})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


def checkout(request):
    return render(request, 'app/checkout.html')


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'Profile has been Updated Successfully!!')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

