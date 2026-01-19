"""
URL configuration for Weiboo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Weiboo import homeViews
from Weiboo import blogViews
from Weiboo import pagesViews
from Weiboo import shopViews

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', homeViews.index, name ='index'),
    path('all-category', homeViews.allCategory, name='allCategory'),
    path('category', homeViews.category, name='category'),
    path('external-products', homeViews.externalProducts, name='externalProducts'),
    path('index', homeViews.index, name='index'),
    path('index-eight', homeViews.indexEight, name='indexEight'),
    path('index-five', homeViews.indexFive, name='indexFive'),
    path('index-four', homeViews.indexFour, name='indexFour'),
    path('index-nine', homeViews.indexNine, name='indexNine'),
    path('index-seven', homeViews.indexSeven, name='indexSeven'),
    path('index-six', homeViews.indexSix, name='indexSix'),
    path('index-ten', homeViews.indexTen, name='indexTen'),
    path('index-three', homeViews.indexThree, name='indexThree'),
    path('index-two', homeViews.indexTwo, name='indexTwo'),
    path('login', homeViews.login, name='login'),
    path('out-of-stock-products', homeViews.outOfStockProducts, name='outOfStockProducts'),
    path('shop-five-column', homeViews.shopFiveColumn, name='shopFiveColumn'),
    path('simple-products', homeViews.simpleProducts, name='simpleProducts'),
    path('thankYou', homeViews.thankYou, name='thankYou'),
    path('wishlist', homeViews.wishlist, name='wishlist'),

    # blog
    path('contact', blogViews.contact, name='contact'),
    path('news', blogViews.news, name='news'),
    path('news-details', blogViews.newsDetails, name='newsDetails'),
    path('news-grid', blogViews.newsGrid, name='newsGrid'),

    # pages
    path('about', pagesViews.about, name='about'),
    path('error-page', pagesViews.errorPage, name='errorPage'),
    path('faq', pagesViews.faq, name='faq'),

    # shop
    path('account', shopViews.account, name='account'),
    path('cart', shopViews.cart, name='cart'),
    path('check-out', shopViews.checkOut, name='checkOut'),
    path('full-width-shop', shopViews.fullWidthShop, name='fullWidthShop'),
    path('grouped-products', shopViews.groupedProducts, name='groupedProducts'),
    path('product-details', shopViews.productDetails, name='productDetails'),
    path('product-details2', shopViews.productDetails2, name='productDetails2'),
    path('shop', shopViews.shop, name='shop'),
    path('sidebar-left', shopViews.sidebarLeft, name='sidebarLeft'),
    path('sidebar-right', shopViews.sidebarRight, name='sidebarRight'),
    path('variable-products', shopViews.variableProducts, name='variableProducts'),

]
