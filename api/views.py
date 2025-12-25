from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListAPIView
from ecommerce.models import Category, Order,Product, UserAddress
from cms.models import slider
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response






from .serializers import PaymentSuccessSerializer, RegisterSerializer, CustomTokenObtainPairSerializer,UpdateProfileSerializer,RequestOTPSerializer, VerifyOTPChangePasswordSerializer,CategorySerializer,SliderSerializer,ProductSerializer,ProductSearchListSerializer,UserAddressSerializer,OrderSerializer,OrderCreateSerializer,UserAddressSerializer
import random
from django.core.mail import send_mail
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import EmailOTP


User = get_user_model()


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
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by("order", "name")


class BannerListView(ListAPIView):
    serializer_class = SliderSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return slider.objects.filter(
            status="active",
            ad_start_date__lte=today,
            ad_end_date__gte=today
        ).select_related(
            "product",
            "slidercat"
        ).order_by("order")


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
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {
                    "message": "Order created successfully",
                    "order_id": order.id
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data)
    


    

class PaymentSuccessAPIView(APIView):
    authentication_classes = [JWTAuthentication]
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
        ).update(paid=True)

        return Response(
            {"message": "Payment successful. Order confirmed."},
            status=status.HTTP_200_OK
        )

