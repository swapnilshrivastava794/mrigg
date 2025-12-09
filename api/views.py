from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer,UpdateProfileSerializer,RequestOTPSerializer, VerifyOTPChangePasswordSerializer
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

