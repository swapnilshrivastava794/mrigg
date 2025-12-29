
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from mriigproject import settings
from mriigproject import views

from django.contrib import admin
from django.urls import path
from mriigproject import homeViews
from mriigproject import blogViews
from mriigproject import pagesViews
from mriigproject import shopViews
from cms import views as cms_views

urlpatterns = [
        
        # Add this line for API section
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', views.home, name='home'),
    # path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('login/', views.custom_login, name='login'),
    # path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),  # ✅ Add this line
    path('profile/', views.profile_view, name='profile'),

        # ✅ Cart & Checkout

    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    # Wishlist URLs
    path('add-to-wishlist/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('wishlist', views.view_wishlist, name='wishlist'),  # Alias for backward compatibility
#static path----
    path('about-us', views.aboutus, name='about-us'),
    path('our-product', views.ourproduct, name='our-product'),
    path('contact-us', views.contactus, name='contact-us'),
    path('order-history/', views.order_history, name='order_history'),
    path('contact/', views.contact_view, name='contact'),


    #  path('news', views.news, name='news'),

    # path('', homeViews.index, name ='index'),
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
    path('wishlist-old', homeViews.wishlist, name='wishlist-old'),  # Keep old for backward compatibility

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
    
    # CMS pages - must come before category URLs to avoid conflicts
    path('<slug:slug>/', cms_views.cms_page, name='cms'),
    
    # SEO-friendly category URLs - product detail must come before category URLs
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/<slug:subcategory_slug>/', shopViews.shop, name='category-subcategory'),
    path('<slug:category_slug>/', shopViews.shop, name='category-only'),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # In production, serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
