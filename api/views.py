from django.utils import timezone
from rest_framework import generics
import hashlib
import hmac
import base64
import json
import requests
from django.conf import settings
import razorpay

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListAPIView
from ecommerce.models import Category, Order, Product, UserAddress, Coupon, CouponUsage, Offer, CustomUser
from .authentication import CustomUserJWTAuthentication, generate_tokens_for_user, refresh_access_token
from cms.models import slider
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication







from .serializers import PaymentSuccessSerializer, RegisterSerializer, CustomTokenObtainPairSerializer,UpdateProfileSerializer,RequestOTPSerializer, VerifyOTPChangePasswordSerializer,CategorySerializer,SliderSerializer,ProductSerializer,ProductSearchListSerializer,UserAddressSerializer,OrderSerializer,OrderCreateSerializer,UserAddressSerializer,OfferSerializer
import random
from django.core.mail import send_mail
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import EmailOTP


User = get_user_model()


# ==================== CUSTOM USER AUTH (Separate from Django Admin) ====================

class CustomUserSignupView(APIView):
    """
    Signup API for CustomUser model.
    This is SEPARATE from Django Admin auth.
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # 👈 Added to fix 403 Forbidden
    
    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')
        mobile = request.data.get('mobile', '').strip()
        username = request.data.get('username', '').strip()
        first_name = request.data.get('first_name', '').strip()
        last_name = request.data.get('last_name', '').strip()
        
        # Validation
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not password or len(password) < 6:
            return Response({'error': 'Password must be at least 6 characters'}, status=status.HTTP_400_BAD_REQUEST)
        if not mobile:
            return Response({'error': 'Mobile is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if mobile already exists
        if CustomUser.objects.filter(mobile=mobile).exists():
            return Response({'error': 'Mobile number already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check username if provided
        if username and CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user
        user = CustomUser(
            email=email,
            mobile=mobile,
            username=username or email.split('@')[0],  # Default username from email
            first_name=first_name,
            last_name=last_name,
            role='customer',
        )
        user.set_password(password)
        user.save()
        
        # Generate JWT tokens
        tokens = generate_tokens_for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'mobile': user.mobile,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            },
            'access': tokens['access'],
            'refresh': tokens['refresh'],
        }, status=status.HTTP_201_CREATED)


class CustomUserLoginView(APIView):
    """
    Login API for CustomUser model.
    This is SEPARATE from Django Admin auth.
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # 👈 Added to fix 403 Forbidden
    
    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')
        
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check password
        if not user.check_password(password):
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is active
        if not user.is_active:
            return Response({'error': 'Account is deactivated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate JWT tokens
        tokens = generate_tokens_for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'mobile': user.mobile,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'date_of_birth': user.date_of_birth,
                'gender': user.gender,
                'address_line1': user.address_line1,
                'address_line2': user.address_line2,
                'city': user.city,
                'state': user.state,
                'zip_code': user.zip_code,
                'country': user.country,
                'profile_image': request.build_absolute_uri(user.profile_image.url) if user.profile_image else None,
            },
            'access': tokens['access'],
            'refresh': tokens['refresh'],
        }, status=status.HTTP_200_OK)


class CustomUserRefreshTokenView(APIView):
    """
    Refresh access token using refresh token.
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # 👈 Added to fix 403 Forbidden
    
    def post(self, request):
        refresh_token = request.data.get('refresh', '')
        
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            new_tokens = refresh_access_token(refresh_token)
            return Response(new_tokens, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class CustomUserProfileView(APIView):
    """
    Get/Update profile for CustomUser.
    """
    authentication_classes = [CustomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'mobile': user.mobile,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'date_of_birth': user.date_of_birth,
            'gender': user.gender,
            'address_line1': user.address_line1,
            'address_line2': user.address_line2,
            'city': user.city,
            'state': user.state,
            'zip_code': user.zip_code,
            'country': user.country,
            'profile_image': request.build_absolute_uri(user.profile_image.url) if user.profile_image else None,
        })
    
    def put(self, request):
        user = request.user
        
        # Update allowed fields
        allowed_fields = [
            'first_name', 'last_name', 'mobile', 'date_of_birth', 'gender',
            'address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country'
        ]
        
        for field in allowed_fields:
            if field in request.data:
                setattr(user, field, request.data[field])
        
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        
        user.save()
        
        return Response({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'mobile': user.mobile,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'date_of_birth': user.date_of_birth,
                'gender': user.gender,
                'address_line1': user.address_line1,
                'address_line2': user.address_line2,
                'city': user.city,
                'state': user.state,
                'zip_code': user.zip_code,
                'country': user.country,
                'profile_image': request.build_absolute_uri(user.profile_image.url) if user.profile_image else None,
            }
        })


# ==================== OLD AUTH VIEWS (Django Default User) ====================

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    # allow login using email
    def post(self, request, *args, **kwargs):
        if 'email' in request.data and 'username' not in request.data:
            data = request.data.copy()
            data['username'] = data['email']   # because USERNAME_FIELD = email
            request._full_data = data
        return super().post(request, *args, **kwargs)


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "mobile": user.mobile,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name,

            "date_of_birth": user.date_of_birth,
            "gender": user.gender,
            "address_line1": user.address_line1,
            "address_line2": user.address_line2,
            "city": user.city,
            "state": user.state,
            "zip_code": user.zip_code,
            "country": user.country,

            "profile_image": request.build_absolute_uri(user.profile_image.url) if user.profile_image else None,
        })


class UpdateProfileView(generics.UpdateAPIView):
     authentication_classes = [JWTAuthentication]   # 🔥 THIS WAS MISSING
     permission_classes = [IsAuthenticated]
     serializer_class = UpdateProfileSerializer

     def get_object(self):
        return self.request.user



# 1) Request OTP
class RequestOTPView(generics.GenericAPIView):
    serializer_class = RequestOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = random.randint(100000, 999999)

        EmailOTP.objects.create(email=email, otp=otp)

        # send OTP email (dummy)
        print("OTP sent to email:", otp)

        return Response({"message": "OTP sent to email"}, status=200)


# 2) Verify OTP & Change Password
class VerifyOTPChangePasswordView(generics.GenericAPIView):
    serializer_class = VerifyOTPChangePasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']

        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # delete OTPs for security
        EmailOTP.objects.filter(email=email).delete()

        return Response({"message": "Password changed successfully"}, status=200)


class ResendOTPView(generics.GenericAPIView):
    serializer_class = RequestOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = random.randint(100000, 999999)

        EmailOTP.objects.create(email=email, otp=otp)

        print("OTP re-sent:", otp)

        return Response({"message": "OTP resent successfully"}, status=200)



class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")

        if not refresh:
            return Response({"error": "Refresh token required"}, status=400)

        token = RefreshToken(refresh)
        token.blacklist()  # 🔥 disables token

        return Response({"message": "Logged out successfully"}, status=200)


class CategoryListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by("order", "name")


class BannerListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SliderSerializer

    def get_queryset(self):
        from django.db.models import Value, IntegerField
        from django.db.models.functions import Coalesce
        from django.db.models import Q
        today = timezone.now().date()
        return slider.objects.filter(
            status="active"
        ).filter(
            # Only show sliders that have at least one media (image or video)
            Q(sliderimage__isnull=False) | Q(slidervideo__isnull=False) | Q(video_url__isnull=False)
        ).filter(
            # Filter by date range if dates are set
            Q(ad_start_date__isnull=True) | Q(ad_start_date__lte=today),
            Q(ad_end_date__isnull=True) | Q(ad_end_date__gte=today)
        ).select_related(
            "product",
            "slidercat"
        ).annotate(
            order_value=Coalesce('order', Value(999999, output_field=IntegerField()))
        ).order_by("order_value", "id")


class ProductsByCategoryAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category_id):

        # 🔹 pagination params
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))

        # 1️⃣ Category ki saari sub-categories
        from ecommerce.models import SubCategory
        subcategory_ids = SubCategory.objects.filter(
            category_id=category_id,
            is_active=True
        ).values_list("id", flat=True)

        # 2️⃣ Subcategories ke products (DESC ORDER)
        queryset = Product.objects.filter(
            subcategory_id__in=subcategory_ids,
            is_active=True,
            available=True
        ).order_by("-id")   # 👈 DESCENDING

        # 4️⃣ Pagination
        paginator = Paginator(queryset, limit)

        try:
            products_page = paginator.page(page)
        except EmptyPage:
            return Response({
                "count": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page,
                "results": []
            })

        serializer = ProductSerializer(
            products_page,
            many=True,
            context={"request": request}
        )

        return Response({
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page,
            "results": serializer.data
        })



class ProductDetailByIdAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request, id):
        product = get_object_or_404(
            Product,
            id=id,
            is_active=True,
            available=True
        )

        serializer = ProductSerializer(
            product,
            context={"request": request}
        )
        return Response(serializer.data)


class HomeProductsAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        popular_products = Product.objects.filter(
            popular=True,
            is_active=True,
            available=True
        ).order_by("-id")[:10]

        latest_products = Product.objects.filter(
            latest=True,
            is_active=True,
            available=True
        ).order_by("-id")[:10]

        featured_products = Product.objects.filter(
            featured=True,
            is_active=True,
            available=True
        ).order_by("-id")[:10]

        return Response({
            "popular": ProductSerializer(
                popular_products,
                many=True,
                context={"request": request}
            ).data,

            "latest": ProductSerializer(
                latest_products,
                many=True,
                context={"request": request}
            ).data,

            "featured": ProductSerializer(
                featured_products,
                many=True,
                context={"request": request}
            ).data,
        })


class FilterProductsAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, type):

        # ✅ validate type
        if type not in ["latest", "featured", "popular"]:
            return Response(
                {"error": "type must be one of latest, featured, popular"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ pagination params
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))

        # ✅ base queryset (DESCENDING ORDER)
        queryset = Product.objects.filter(
            **{
                type: True,
                "is_active": True,
                "available": True
            }
        ).order_by("-id")   # 👈 DESC ORDER (latest first)

        # ✅ paginator
        paginator = Paginator(queryset, limit)

        try:
            products_page = paginator.page(page)
        except EmptyPage:
            return Response({
                "count": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page,
                "results": []
            })

        serializer = ProductSerializer(
            products_page,
            many=True,
            context={"request": request}
        )

        return Response({
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page,
            "results": serializer.data
        })
    

class ProductSearchListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSearchListSerializer

    def get_queryset(self):
        request = self.request
        query = request.GET.get("q", "").strip()

        # Amazon / Flipkart behavior
        if not query:
            return Product.objects.none()

        return Product.objects.filter(
            is_active=True,
            available=True
        ).select_related(
            "subcategory",
            "subcategory__category"
        ).prefetch_related(
            "images"     # ✅ variations NOT needed in listing
        ).filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(subcategory__name__icontains=query) |
            Q(subcategory__category__name__icontains=query)
        ).order_by("-created")
    

# ordrrelated api
class UserAddressListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = UserAddress.objects.filter(user=request.user)
        serializer = UserAddressSerializer(addresses, many=True)
        return Response(serializer.data)
    
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserAddressAPIView(APIView):
    authentication_classes = [CustomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    # 📌 GET → List addresses
    def get(self, request):
        addresses = UserAddress.objects.filter(user=request.user)
        serializer = UserAddressSerializer(addresses, many=True)
        return Response(serializer.data)

    # 📌 POST → Create address
    def post(self, request):
        serializer = UserAddressSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data.get("is_default"):
                UserAddress.objects.filter(
                    user=request.user, is_default=True
                ).update(is_default=False)

            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserAddressDetailAPIView(APIView):
    authentication_classes = [CustomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, user, pk):
        return UserAddress.objects.get(pk=pk, user=user)

    # 📌 PUT → Update address
    def put(self, request, pk):
        address = self.get_object(request.user, pk)
        serializer = UserAddressSerializer(address, data=request.data, partial=True)

        if serializer.is_valid():
            if serializer.validated_data.get("is_default"):
                UserAddress.objects.filter(
                    user=request.user, is_default=True
                ).update(is_default=False)

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 📌 DELETE → Delete address
    def delete(self, request, pk):
        address = self.get_object(request.user, pk)
        address.delete()
        return Response({"message": "Address deleted"}, status=status.HTTP_204_NO_CONTENT)

    
class CheckoutView(APIView):
    authentication_classes = [CustomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            order = serializer.save()
            
            # 🟢 DIRECT SUCCESS (Bypass Payment Gateway)
            order.paid = True
            order.status = 'paid'
            order.save()
            
            # Calculate details for response
            subtotal = order.get_total_cost()
            discount = order.discount_total
            final_total = subtotal - discount
            
            # Collect multiple coupons if used
            coupon_codes = []
            if order.coupons.exists():
                coupon_codes = [c.code for c in order.coupons.all()]
            elif order.coupon: # Fallback
                coupon_codes = [order.coupon.code]

            return Response(
                {
                    "message": "Order placed successfully. Payment Successful.",
                    "order_id": order.id,
                    "original_total_amount": subtotal,
                    "coupon_discount_amount": discount,
                    "final_payable_amount": final_total,
                    "applied_coupons": coupon_codes,
                    "payment_status": "Success"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyOrdersView(APIView):
    authentication_classes = [CustomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        status_param = request.GET.get('status')   # delivered, shipped, cancelled
        search = request.GET.get('search')         # nike, puma, sony

        orders = Order.objects.filter(user=user)

        # 🔹 STATUS FILTER (Tabs ke liye)
        if status_param and status_param != 'all':
            orders = orders.filter(status=status_param)

        # 🔹 SEARCH (product name OR order id)
        if search:
            orders = orders.filter(
                Q(items__product__name__icontains=search) |
                Q(id__icontains=search)
            ).distinct()

        orders = orders.order_by('-created')

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class OrderDetailView(APIView):
    authentication_classes = [CustomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user
        )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CancelOrderAPIView(APIView):
    authentication_classes = [CustomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user
        )

        # 🔒 CANCEL RULE
        if order.status not in ['created', 'paid']:
            return Response(
                {"error": "Order cannot be cancelled at this stage"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'cancelled'
        order.save()

        return Response(
            {"message": "Order cancelled successfully"},
            status=status.HTTP_200_OK
        )

    


    

class PaymentSuccessAPIView(APIView):
    authentication_classes = [CustomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentSuccessSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']

        Order.objects.filter(
            id=order_id,
            user=request.user,
            paid=False
        ).update(
            paid=True,
            status='paid'
        )

        return Response(
            {"message": "Payment successful. Order confirmed."},
            status=status.HTTP_200_OK
        )


from ecommerce.models import Order, Payment # Ensure Payment is imported

class GokwikPaymentInitiateView(APIView):
    authentication_classes = [CustomUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'error': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Gokwik Configuration
        merchant_id = getattr(settings, 'GOKWIK_MERCHANT_ID', '')
        app_id = getattr(settings, 'GOKWIK_APP_ID', '')
        app_secret = getattr(settings, 'GOKWIK_APP_SECRET', '')
        
        if not all([merchant_id, app_id, app_secret]):
             return Response({'error': 'Gokwik credentials not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        amount = order.get_total_cost()

        # 1. Create Payment Record (Pending)
        payment = Payment.objects.create(
            order=order,
            amount=amount,
            status='pending',
            payment_method='gokwik'
        )

        # Payload Construction
        payload = {
            'merchant_id': merchant_id,
            'app_id': app_id,
            'order_id': str(order.id),
            'amount': str(amount),
            'currency': 'INR',
            'customer_name': request.user.first_name,
            'customer_email': request.user.email,
            'customer_phone': getattr(request.user, 'mobile', ''),
            'timestamp': str(timezone.now().timestamp()),
            # Pass Payment ID to track it back if needed, or rely on Order ID
            'merchant_param1': str(payment.id) 
        }
        
        # Signature Generation
        payload_string = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            key=app_secret.encode(),
            msg=payload_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        return Response({
            'payload': payload,
            'signature': signature,
            'url': getattr(settings, 'GOKWIK_BASE_URL', '') + '/checkout'
        }, status=status.HTTP_200_OK)


class GokwikPaymentCallbackView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        data = request.data
        
        # 1. Extract Data
        gokwik_payment_id = data.get('gokwik_payment_id')
        status_value = data.get('status')
        amount = data.get('amount')
        order_id = data.get('order_id')
        payment_id = data.get('merchant_param1') # We sent this

        try:
            # 2. Find the Payment Record
            # Try via Payment ID first (more precise), then Order ID
            if payment_id:
                payment = Payment.objects.get(id=payment_id)
            else:
                # Fallback: Find latest pending payment for this order
                payment = Payment.objects.filter(order_id=order_id, status='pending').last()
                
            if not payment:
                 return Response({'status': 'error', 'message': 'Payment Record Not Found'}, status=status.HTTP_404_NOT_FOUND)

            # 3. Update Payment Status
            payment.gokwik_oid = gokwik_payment_id
            payment.response_data = json.dumps(data)
            
            if status_value == 'SUCCESS':
                payment.status = 'success'
                payment.transaction_id = gokwik_payment_id
                payment.save()
                
                # 4. Update Main Order
                order = payment.order
                order.paid = True
                order.status = 'paid'
                order.save()
            else:
                payment.status = 'failed'
                payment.save()
            
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)

        except Exception as e:
             return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApplyCouponAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        cart_total_param = request.data.get('cart_total') # Optional legacy
        items = request.data.get('items') # New Payload: [{product_id: 1, total_price: 500}]

        if not code:
             return Response({"valid": False, "error": "Coupon code is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return Response({"valid": False, "error": "Invalid coupon code"}, status=status.HTTP_404_NOT_FOUND)

        if not coupon.active:
             return Response({"valid": False, "error": "Coupon is inactive"}, status=status.HTTP_200_OK)

        # Calculate Eligible Amount
        eligible_amount = 0.0
        total_cart_value = 0.0
        
        if items and isinstance(items, list):
            # 1. Fetch restrictions
            valid_product_ids = set(coupon.valid_products.values_list('id', flat=True))
            valid_category_ids = set(coupon.valid_categories.values_list('id', flat=True))
            
            has_restrictions = bool(valid_product_ids or valid_category_ids)
            
            # 2. Fetch all products in cart for attribute checking
            cart_product_ids = [item.get('product_id') for item in items if item.get('product_id')]
            products_map = {p.id: p for p in Product.objects.filter(id__in=cart_product_ids).select_related('subcategory__category')}
            
            for item in items:
                try:
                    p_id = item.get('product_id')
                    price = float(item.get('total_price', 0))
                    total_cart_value += price
                    
                    # If no restrictions, applies to all
                    if not has_restrictions:
                        eligible_amount += price
                        continue

                    is_eligible = False
                    
                    # Check Product Restriction
                    if p_id in valid_product_ids:
                        is_eligible = True
                    
                    # Check Category Restriction
                    elif p_id in products_map:
                        product = products_map[p_id]
                        if product.subcategory.category.id in valid_category_ids:
                            is_eligible = True
                    
                    if is_eligible:
                        eligible_amount += price
                        
                except (ValueError, TypeError):
                    continue
        
        elif cart_total_param is not None:
             # Legacy / Manual Total Fallback
             try:
                eligible_amount = float(cart_total_param)
                total_cart_value = eligible_amount
             except ValueError:
                return Response({"valid": False, "error": "Invalid cart total"}, status=status.HTTP_400_BAD_REQUEST)
        else:
             return Response({"valid": False, "error": "Either items or cart_total is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check Min Purchase on ELIGIBLE Amount (or Total? user intent varies. usually eligible)
        # Assuming min_purchase applies to the items getting the discount
        if eligible_amount < coupon.min_purchase_amount:
            return Response({"valid": False, "error": f"Minimum purchase of ₹{coupon.min_purchase_amount} required on applicable items"}, status=status.HTTP_200_OK)

        # Calculate Discount
        discount = coupon.calculate_discount(eligible_amount)

        return Response({
            "valid": True,
            "code": coupon.code,
            "discount_amount": discount,
            "discount_type": coupon.discount_type, # 'percent' or 'flat'
            "message": f"Coupon applied! You saved ₹{discount}"
        }, status=status.HTTP_200_OK)


class OfferListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = OfferSerializer

    def get_queryset(self):
        queryset = Offer.objects.filter(is_active=True).order_by('order', '-created_at')
        
        # Filter by Page Position
        page_position = self.request.query_params.get('page_position')
        if page_position:
            queryset = queryset.filter(page_position=page_position)

        # Filter by Offer Name (Type)
        offer_name = self.request.query_params.get('offer_name')
        if offer_name:
            queryset = queryset.filter(offer_name=offer_name)

        # Filter by Date Validity
        now = timezone.now()
        queryset = queryset.filter(start_date__lte=now, end_date__gte=now)

        return queryset


class OfferDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = OfferSerializer
    lookup_field = 'id'

    def get_queryset(self):
        now = timezone.now()
        return Offer.objects.filter(is_active=True, start_date__lte=now, end_date__gte=now)


class RazorpayOrderCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'error': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, id=order_id, user=request.user)
        amount = int(order.get_total_cost() * 100)  # Amount in paise

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        data = {
            "amount": amount,
            "currency": "INR",
            "receipt": f"order_rcptid_{order.id}",
            "notes": {
                "order_id": order.id,
                "user_email": request.user.email
            }
        }

        try:
            razorpay_order = client.order.create(data=data)
            
            # Create Payment record
            Payment.objects.create(
                order=order,
                amount=order.get_total_cost(),
                status='pending',
                payment_method='razorpay',
                razorpay_order_id=razorpay_order['id']
            )

            return Response({
                'id': razorpay_order['id'],
                'amount': razorpay_order['amount'],
                'currency': razorpay_order['currency'],
                'keyId': settings.RAZORPAY_KEY_ID
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RazorpayPaymentVerifyAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            # Verify signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            client.utility.verify_payment_signature(params_dict)

            # Update Payment Record
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'success'
            payment.save()

            # Update Order Status
            order = payment.order
            order.paid = True
            order.status = 'paid'
            order.save()

            return Response({'status': 'Payment successful'}, status=status.HTTP_200_OK)

        except razorpay.errors.SignatureVerificationError:
            payment = Payment.objects.filter(razorpay_order_id=razorpay_order_id).first()
            if payment:
                payment.status = 'failed'
                payment.save()
            return Response({'error': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
             return Response({'error': 'Payment record not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Validate other general rules (Date, Usage)
        is_valid, message = coupon.is_valid(cart_total=total_cart_value, user=request.user)
        if not is_valid:
             return Response({"valid": False, "error": message}, status=status.HTTP_200_OK)

        # Calculate Discount
        discount = coupon.calculate_discount(eligible_amount)
        
        # Ensure we don't return negative total
        new_total = max(0, total_cart_value - discount)

        return Response({
            "valid": True,
            "message": "Coupon applied successfully",
            "code": coupon.code,
            "discount_amount": discount,
            "discount_type": coupon.discount_type,
            "new_total": new_total,
            "coupon_id": coupon.id
        }, status=status.HTTP_200_OK)


class UserdelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, cusuid_id):
        """
        Deactivate and anonymize a user by ID (Google Play Compliant).
        """
        try:
            # Get the user to be deactivated
            user_to_deactivate = get_object_or_404(CustomUser, id=cusuid_id)
            
            # Check permissions
            if request.user.id != user_to_deactivate.id:
                if not (request.user.is_staff or request.user.is_superuser):
                    return Response(
                        {"error": "You don't have permission to deactivate this user"},
                        status=status.HTTP_403_FORBIDDEN
                    )
            
            # Anonymize User Data (GDPR/Google Play Compliant)
            timestamp = int(timezone.now().timestamp())
            
            user_to_deactivate.first_name = "Deleted"
            user_to_deactivate.last_name = "User"
            user_to_deactivate.email = f"deleted_{user_to_deactivate.id}_{timestamp}@mriigg.deleted"
            user_to_deactivate.username = f"deleted_{user_to_deactivate.id}_{timestamp}"
            
            if hasattr(user_to_deactivate, 'mobile'):
                user_to_deactivate.mobile = f"0000000000" # Nullify mobile

            # Clear address or other personal info if needed
            user_to_deactivate.address_line1 = ""
            user_to_deactivate.address_line2 = ""
            user_to_deactivate.city = ""
            user_to_deactivate.state = ""
            
            # Deactivate
            user_to_deactivate.is_active = False
            user_to_deactivate.save()
            
            # Optionally: Delete social auth tokens or sessions here
            
            return Response(
                {"message": "Account deleted and data anonymized successfully"},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"error": f"Error deleting user: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


