from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CancelOrderAPIView,
    CheckoutView,
    MyOrdersView,
    OrderDetailView,
    PaymentSuccessAPIView,
    ProductSearchListView,
    RegisterView,
    CustomTokenObtainPairView,
    ProfileView,
    UpdateProfileView,
    RequestOTPView,
    UserAddressAPIView,
    UserAddressDetailAPIView,
    UserAddressListView,
    VerifyOTPChangePasswordView,
    LogoutView,
    ResendOTPView,

    CategoryListView,
    BannerListView,

    ProductsByCategoryAPI,
    ProductDetailByIdAPI,
    HomeProductsAPI,
    FilterProductsAPI,
    GokwikPaymentInitiateView,
    GokwikPaymentCallbackView,
    ApplyCouponAPI
)

urlpatterns = [

    # ================= AUTH =================
    path("auth/register/", RegisterView.as_view(), name="api_register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="api_login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="api_refresh"),
    path("auth/me/", ProfileView.as_view(), name="api_me"),
    path("auth/update-profile/", UpdateProfileView.as_view(), name="api_update_profile"),
    path("auth/request-otp/", RequestOTPView.as_view(), name="api_request_otp"),
    path(
        "auth/verify-otp-change-password/",
        VerifyOTPChangePasswordView.as_view(),
        name="api_verify_otp_change_password",
    ),
    path("auth/resend-otp/", ResendOTPView.as_view(), name="api_resend_otp"),
    path("auth/logout/", LogoutView.as_view(), name="api_logout"),

    # ================= PUBLIC DATA =================
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("banners/", BannerListView.as_view(), name="banner_list"),

    # ================= PRODUCTS (ID BASED, NO LOGIN) =================
    # 👉 category_id param do → us category ke saare products milenge
    path(
        "products/<int:category_id>/",
        ProductsByCategoryAPI.as_view(),
        name="products_by_category_id",
    ),

    # 👉 single product detail (ID based)
    path(
        "product/<int:id>/",
        ProductDetailByIdAPI.as_view(),
        name="product_detail_by_id",
    ),

     path(
        "home/products/",
        HomeProductsAPI.as_view(),
        name="home_products",
    ),

    path(
    "product/<str:type>/",
    FilterProductsAPI.as_view(),
    name="product_filter_by_type",

),
    path("products/search/", ProductSearchListView.as_view(), name="product-search"),

    path('addresses/', UserAddressListView.as_view(), name='address-list'),
    path("user/addresses/", UserAddressAPIView.as_view()),
    path("user/addresses/<int:pk>/", UserAddressDetailAPIView.as_view()),

    path('checkout/', CheckoutView.as_view(), name='checkout'),

    path('orders/', MyOrdersView.as_view(), name='my-orders'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/cancel/', CancelOrderAPIView.as_view(), name='cancel-order'),


    path("payment-success/", PaymentSuccessAPIView.as_view(), name="payment-success"),
    
    # Gokwik
    path("gokwik/initiate/", GokwikPaymentInitiateView.as_view(), name="gokwik-initiate"),
    path("gokwik/callback/", GokwikPaymentCallbackView.as_view(), name="gokwik-callback"),
    
    # Coupon
    path("coupon/apply/", ApplyCouponAPI.as_view(), name="coupon-apply"),
]
