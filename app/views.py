from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from app import views
from django.views import View  # importing View class
from .models import CATEGORY_CHOICES, Customer, Preorder, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required #for functions based views
from django.utils.decorators import method_decorator #for class based views
from django.core.mail import send_mail

class ProductView(View):
    def get(self, request):
        total_items = 0
        # the given filters the products on the basis of category TW
        tshirts = Product.objects.filter(category='T')  # TW=Top wear
        jeans = Product.objects.filter(category='JE')
        shoes = Product.objects.filter(category='S')
        trousers = Product.objects.filter(category='Tr')
        jackets = Product.objects.filter(category='J')
        onepiece = Product.objects.filter(category='OP')
        ladies_shoes = Product.objects.filter(category='LS')
        ladies_pants = Product.objects.filter(category='LP')
        tops = Product.objects.filter(category='TO')
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
        context = {'tshirts': tshirts, 'trousers':trousers,'jackets':jackets,
                   'jeans': jeans,'shoes':shoes,'total_items':total_items,'tops':tops}
        return render(request, 'app/home.html', context)


class ProductDetailView(View):
    def get(self, request, pk):
        total_items = 0
        product = Product.objects.get(pk=pk)
        all = Product.objects.all()
        item_in_cart = False
        if request.user.is_authenticated:
            total_items = len(Cart.objects.filter(user=request.user))
            item_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        context = {'product': product,'item_in_cart':item_in_cart,'total_items':total_items,'all':all}
        return render(request, 'app/productdetail.html', context)
        
@login_required
def add_to_cart(request):
    user = request.user  # fetching current users
    # fetching product id from product_detail page
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)  # getting product instance
    size = request.GET.get('prod_size')
    # email = request.user.email
    # send_mail(
    #     'Added to cart', # subject
    #     'New products added by', #message
    #     email, #from
    #     ['nepali.mohan11@gmail.com'], #to
    # )
    Cart(user=user, product=product, size=size).save()  # saving Cart data in database
    return redirect('/cart')
    # return render(request, 'app/addtocart.html')

@login_required
def add_to_preorder(request):
    user = request.user  # fetching current users
    # fetching product id from product_detail page
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)  # getting product instance
    size = request.GET.get('prod_size')
    email = request.user.email
    send_mail(
        'Preorder', # subject
        'New Preorder added ', #message
        email, #from
        ['nepali.mohan11@gmail.com'], #to
        fail_silently=False,
    )
    Preorder(user=user, product=product, size=size).save()  # saving Cart data in database
    return redirect('/preorder')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 20.0
        total_amount = 0.0
        #list comprehension to store cart data of authenticated user
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount+= temp_amount
                total_items = len(Cart.objects.filter(user=request.user))
                total_amount = amount + shipping_amount
                context = {'carts': cart,'total_amount':total_amount,'amount':amount, 'total_items':total_items,'shipping_amount':shipping_amount}
            return render(request, 'app/addtocart.html', context)
        else:
            return render(request, 'app/emptycart.html')

@login_required
def preorder(request):
    if request.user.is_authenticated:
        user = request.user
        preorder = Preorder.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 10.0
        total_amount = 0.0
        total_items = 0.0
        #list comprehension to store cart data of authenticated user
        preorder_product = [p for p in Preorder.objects.all() if p.user == user]

        if preorder_product:
            for p in preorder_product:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount+= temp_amount
                total_items = len(Preorder.objects.filter(user=request.user))
                total_amount = amount + shipping_amount
                context = {'preorder': preorder,'total_items':total_items,'active':'btn-primary'}
            return render(request, 'app/preorder.html', context)
        else:
            total_items = len(Preorder.objects.filter(user=request.user))
            return render(request, 'app/preorder.html',{'total_items':total_items})
            
            

def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id'] #getting info stored in prod_id from myscript.js
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 10.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount+= temp_amount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id'] #getting info stored in prod_id from myscript.js
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 10.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount+= temp_amount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id'] #getting info stored in prod_id from myscript.js
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 10.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount+= temp_amount
        data = {
            'amount':amount,
            'totalamount':amount + shipping_amount

            }
        return JsonResponse(data)


@login_required
def remove_preorder(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id'] #getting info stored in prod_id from myscript.js
        print(prod_id)
        c = Preorder.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 10.0
        cart_product = [p for p in Preorder.objects.all() if p.user == request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount+= temp_amount
        data = {
            }
        return JsonResponse(data)

def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required
def address(request):
    total_items = len(Cart.objects.filter(user=request.user))
    # filtering customers on the basis of current users
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add,'total_items':total_items,'active':'btn-primary'})

@login_required
def orders(request):
    total_items = len(Cart.objects.filter(user=request.user))
    op = OrderPlaced.objects.filter(user=request.user)
    # product = Product.objects.filter(stock=st)
    return render(request, 'app/orders.html',{'order_placed':op,'total_items':total_items,'active':'btn-primary'})

def trousers(request):
    trousers = Product.objects.filter(category='Tr')
    return render(request, 'app/trousers.html', {'trousers': trousers})

def tshirts(request):
    tshirts = Product.objects.filter(category='T')
    return render(request, 'app/tshirts.html', {'tshirts': tshirts})


def jeans(request):
    jeans = Product.objects.filter(category='JE')
    return render(request, 'app/jeans.html', {'jeans': jeans})

def shoes(request):
    shoes = Product.objects.filter(category='S')
    return render(request, 'app/shoes.html', {'shoes': shoes})

def jackets(request):
    jackets = Product.objects.filter(category='J')
    return render(request, 'app/jackets.html', {'jackets': jackets})

def onepiece(request):
    onepiece = Product.objects.filter(category='OP')
    return render(request, 'app/onepiece.html', {'onepiece': onepiece})

def ladies_shoes(request):
    ladies_shoes = Product.objects.filter(category='LS')
    return render(request, 'app/ladies_shoes.html', {'ladies_shoes': ladies_shoes})

def ladies_pants(request):
    ladies_pants = Product.objects.filter(category='LP')
    return render(request, 'app/ladies_pants.html', {'ladies_pants': ladies_pants})

def tops(request):
    tops = Product.objects.filter(category='TO')
    return render(request, 'app/tops.html', {'tops': tops})


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

@login_required
def checkout(request):
    user = request.user #6:0:1
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    # id = request.GET['prod_id']
    amount = 0.0
    total_items = 0.0
    shipping_amount = 10.0 
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    # email = request.user.email
    # message = "Checkout Clicked by"+ " " + user
    # send_mail(
    #     'Checkout', # subject
    #     message, #message
    #     email, #from
    #     ['nepali.mohan11@gmail.com'], #to
    # )
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            total_items = len(Cart.objects.filter(user=request.user))
            amount+= temp_amount
            totalamount = amount + shipping_amount
            context = {'add':add, 'totalamount':totalamount,'cart_items':cart_items,'total_items':total_items,'id':id}
    return render(request, 'app/checkout.html',context)

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity,size=c.size).save()
        c.delete()
    email = request.user.email
    send_mail(
        'Payment Done', # subject
        'Payment for the product', #message
        ['nepali.mohan11@gmail.com'], #to
        email, #from
    )
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        total_items = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary','total_items':total_items})

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

def search(request, **kwargs):
    if request.method == "GET":
        query = request.GET.get('query')
        total_items = 0
        if query:
            total_items = len(Cart.objects.filter(user=request.user))
            products = Product.objects.filter(title__icontains=query)
            return render(request,'app/search.html',{'products':products, 'total_items':total_items})
        else:
            return render(request,'app/emptysearch.html')
