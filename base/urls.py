from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name = "home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout" ),
    path('movies/', views.Movies, name="movies" ),
    path('shop/', views.Shop, name="shop" ),
    path('cart/', views.myCart, name="cart" ),
    path('add_item/<str:pk>', views.addItem, name="addItem" ),
    path('delete_item/<str:pk>', views.deleteItem, name="deleteItem" ),
    path('checkout/', views.checkout, name="checkout"),
    path('pay/', views.remove, name="remove"),
]