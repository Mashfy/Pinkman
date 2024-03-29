from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q, query
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import time

class ProductView(View):
    def get(self,request):
        totalitem=0
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        laptops=Product.objects.filter(category='L')
        watches=Product.objects.filter(category='W')
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops,'watches':watches,'totalitem':totalitem})

class ProductDeatilView(View):
    def get(self,request,pk):
        totalitem=0
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    cart_product=[p for p in Cart.objects.all() if p.user==user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
            totalamount=amount+shipping_amount
        totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
    else:
        totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/emptycart.html',{'totalitem':totalitem})
    

def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        data={
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)


# def buy_now(request):
#  return render(request, 'app/buynow.html')


@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    if add.exists():
        totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/address.html',{'add':add,'active':'btn-primary','totalitem':totalitem})
    else:
        totalitem=len(Cart.objects.filter(user=request.user))
        return render(request, 'app/emptyaddress.html',{'add':add,'active':'btn-primary','totalitem':totalitem})


@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html',{'order_placed':op,'totalitem':totalitem})


def mobile(request,data=None):
    totalitem=0
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='Apple' or data=='Samsung' or data=='Oppo':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=80000)
    elif data=='above':
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=80000)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def laptop(request,data=None):
    totalitem=0
    if data==None:
        laptops=Product.objects.filter(category='L')
    elif data=='Asus' or data=='HP'or data=='Apple':
        laptops=Product.objects.filter(category='L').filter(brand=data)
    elif data=='below':
        laptops=Product.objects.filter(category='L').filter(discounted_price__lt=110000)
    elif data=='above':
        laptops=Product.objects.filter(category='L').filter(discounted_price__gt=110000)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/laptop.html',{'laptops':laptops,'totalitem':totalitem})

def topwear(request,data=None):
    totalitem=0
    if data==None:
        topwears=Product.objects.filter(category='TW')
    elif data=='JamesPerse' or data=='Calvinklein':
        topwears=Product.objects.filter(category='TW').filter(brand=data)
    elif data=='below':
        topwears=Product.objects.filter(category='TW').filter(discounted_price__lt=3000)
    elif data=='above':
        topwears=Product.objects.filter(category='TW').filter(discounted_price__gt=3000)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/topwear.html',{'topwears':topwears,'totalitem':totalitem})


def bottomwear(request,data=None):
    totalitem=0
    if data==None:
        bottomwears=Product.objects.filter(category='BW')
    elif data=='Armani' or data=='Levis':
        bottomwears=Product.objects.filter(category='BW').filter(brand=data)
    elif data=='below':
        bottomwears=Product.objects.filter(category='BW').filter(discounted_price__lt=6000)
    elif data=='above':
        bottomwears=Product.objects.filter(category='BW').filter(discounted_price__gt=6000)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears,'totalitem':totalitem})


def watch(request,data=None):
    totalitem=0
    if data==None:
        watches=Product.objects.filter(category='W')
    elif data=='Quartz' or data=='Blancpain':
        watches=Product.objects.filter(category='W').filter(brand=data)
    elif data=='below':
        watches=Product.objects.filter(category='W').filter(discounted_price__lt=10000)
    elif data=='above':
        watches=Product.objects.filter(category='W').filter(discounted_price__gt=10000)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/watch.html',{'watches':watches,'totalitem':totalitem})

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})

    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully, please login now.')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})


@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    add=Customer.objects.filter(user=request.user)
    # if add.exists():
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
    totalamount=amount+shipping_amount
    totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitem':totalitem})
    # else:
    #     totalitem=len(Cart.objects.filter(user=request.user))
    #     return render(request, 'app/emptyaddress.html',{'add':add,'active':'btn-primary','totalitem':totalitem})



@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer = None
    try:
        customer=Customer.objects.get(id=custid)
    except Exception as e:
        return redirect('profileadd')
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})
    
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            address=form.cleaned_data['address']
            area=form.cleaned_data['area']
            district=form.cleaned_data['district']
            mobno=form.cleaned_data['mobno']
            reg=Customer(user=usr,name=name,address=address,area=area,district=district,mobno=mobno)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})

@method_decorator(login_required,name='dispatch')
class ProfileViewadd(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})
    
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            address=form.cleaned_data['address']
            area=form.cleaned_data['area']
            district=form.cleaned_data['district']
            mobno=form.cleaned_data['mobno']
            reg=Customer(user=usr,name=name,address=address,area=area,district=district,mobno=mobno)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
            totalitem=len(Cart.objects.filter(user=request.user))
        return redirect('checkout')


def search(request):
    query=request.GET['query']
    allproducts=Product.objects.filter(title__icontains=query)
    if allproducts:
        return render(request, 'app/search.html',{'allproducts':allproducts})
    else:
        return render(request, 'app/emptysearch.html')