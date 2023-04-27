
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from .form import CustomUserForm
from .models import *
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
import json

# Create your views here.
def registration(request):
    form=CustomUserForm()
    if request.method == 'POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,"registration successfull"  + user)
            return redirect('LoginPage')
    context={
        'form':form
    }
    return render(request,'registration.html',context)
def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"login successfull"+ ' '+str(request.user).capitalize())
                return redirect('home')
            else:
                messages.info(request,"Please check the username and password")
    return render(request,'LoginPage.html')
def LogoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out successfully")
        return redirect('home')

def home(request):
    product=Product.objects.filter(trending=1)
    context={
        'product':product
    }
    return render(request,'home.html',context)
def add_to_cart(request):
    if request.headers.get('X-Requested-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            postObj=json.load(request)
            product_qty=postObj['product_qty']
            product_id=postObj['pid']
            # print(request.user)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status': 'product already added in cart'}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status': 'product added to cart'}, status=200)
                    else:
                        return JsonResponse({'status':'product stock not available'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
    
def cart(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        context={
            'cart':cart
        }
        return render(request,'cart.html',context)
    else:
        return redirect('home')
    
def collections(request):
    if 'q' in request.GET:
        q=request.GET['q']
        search=Catagories.objects.filter(name__icontains=q)
    else:
        search=Catagories.objects.filter(status=0)
    context={
        # 'catagory':catagory,
        'search':search
    }
    return render(request,'catagories.html',context)
def collectionview(request,name):
    if(Catagories.objects.filter(name=name,status=0)):
        product=Product.objects.filter(catagories__name=name)
        if 'q' in request.GET:
            q=request.GET['q']
            product=Product.objects.filter(name__icontains=q,catagories__name=name)
        else:
            product=Product.objects.filter(catagories__name=name)
        context={
            'product':product,
            'catagory_name':name
        }
        return render(request,'collections.html',context)
    else:
        messages.warning(request,"no such catagory found")
        return redirect('collections')
def product_detail(request,cname,pname):
    if(Catagories.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            product=Product.objects.filter(name=pname,status=0).first()
            context={
                'product':product
            }
            return render(request,"product_detail.html",context)
        else:
            messages.error(request,"no such product found")
            return redirect('collections')
    else:
        messages.error(request,"no such catagory found")
        return redirect('collections')
def checkout(request):
    return render(request,"checkout.html")
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('cart')
def removefav(request,fid):
    item=favourite.objects.get(id=fid)
    item.delete()
    return redirect('favouritepage')
    
def fav(request):
    if request.headers.get('X-Requested-With')=='XMLHttpRequest':
        if request.user.is_authenticated:
            postObj=json.load(request)
            product_id=postObj['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if favourite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product already in favourite'}, status=200)
                else:
                    favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'product added to favourite'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add Favourite'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

def favouritepage(request):
    if request.user.is_authenticated:
        fav=favourite.objects.filter(user=request.user)
        context={
            'fav':fav
        }
        return render(request,'favouritepage.html',context)
    
    else:
        return redirect('home')