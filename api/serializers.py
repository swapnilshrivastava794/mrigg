from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import EmailOTP
from django.utils import timezone
from datetime import timedelta
from main.models import Category, Banner


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password',
            'mobile',

            # extra fields from your CustomUser
            'first_name',
            'last_name',
            'role',
            'date_of_birth',
            'gender',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'zip_code',
            'country',
            'profile_image',
        ]
        extra_kwargs = {
            'role': {'read_only': True},  # default = customer
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['role'] = user.role
        token['mobile'] = user.mobile
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        # Add full user data in response
        data['user'] = {
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
            "profile_image": self.context['request'].build_absolute_uri(user.profile_image.url) if user.profile_image else None,
        }

        return data


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'mobile',
            'date_of_birth',
            'gender',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'zip_code',
            'country',
            'profile_image',
        ]
        extra_kwargs = {
            'mobile': {'required':False},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)


            instance.save()
            return instance


class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOTPChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    new_password = serializers.CharField(min_length=6)
    
    def validate(self, data):
        email = data['email']
        otp = data['otp']

        try:
            otp_obj = EmailOTP.objects.filter(email=email, otp=otp).latest('created_at')
        except:
            raise serializers.ValidationError("Invalid OTP")

        # check OTP expiry (10 minutes)
        if otp_obj.created_at < timezone.now() - timedelta(minutes=10):
            raise serializers.ValidationError("OTP expired")

        return data


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "image",
            "parent",
            "subcategories",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_subcategories(self, obj):
        children = obj.subcategories.all().order_by("order", "name")
        return CategorySerializer(children, many=True, context=self.context).data


class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ["id", "title", "image", "order"]

    def get_image(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)