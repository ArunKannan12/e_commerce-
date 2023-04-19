from . import views 
from django.urls import path


urlpatterns = [
    path("", views.home, name="home"),
    path("registration/",views.registration, name="registration"),
    path("LoginPage/",views.LoginPage, name="LoginPage"),
    path("collections/",views.collections, name="collections"),
    path("collections/<str:name>",views.collectionview, name="collections"),
    path("collections/<str:cname>/<str:pname>", views.product_detail, name="product_detail"),
    path("checkout/",views.checkout,name="checkout"),
    path("LogoutPage",views.LogoutPage, name="LogoutPage"),
    path("addtocart",views.add_to_cart, name="addtocart"),
    path("cart",views.cart, name="cart"),
    path("removecart/<str:cid>",views.remove_cart,name="removecart"),
    path("fav",views.fav,name="fav"),
    path("favouritepage",views.favouritepage,name="favouritepage"),
    path("removefav<str:fid>",views.removefav,name="removefav"),
]
