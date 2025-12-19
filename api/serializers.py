from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import EmailOTP
from django.utils import timezone
from datetime import timedelta
from ecommerce.models import (
    Category,
    SubCategory,
    Product,
    ProductImage,
    ProductVariation,
    ProductDetailSection,
)

from cms.models import slider

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


class SubCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = [
            "id",
            "name",
            "slug",
            "image",
            "order",
            "is_active",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


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
            "subcategories",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_subcategories(self, obj):
        children = SubCategory.objects.filter(category=obj, is_active=True).order_by("order", "name")
        return SubCategorySerializer(children, many=True, context=self.context).data


class SliderSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = slider
        fields = [
            "id",
            "ad_title",
            "ad_description",
            "image",          # frontend-friendly key
            "deal_type",
            "slug",
            "order",
            "status",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.sliderimage and request:
            return request.build_absolute_uri(obj.sliderimage.url)
        return None



class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class ProductVariationSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariation
        fields = [
            "id",
            "name",
            "quantity",
            "unit",
            "is_sku_code",
            "color_code",
            "slug",
            "price_modifier",
            "offerprice",
            "stock",
            "final_price",
        ]

    def get_final_price(self, obj):
        base_price = obj.product.price
        price = base_price + (obj.price_modifier or 0)

        if obj.offerprice and obj.offerprice > 0:
            return obj.offerprice

        return price




class ProductDetailSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetailSection
        fields = [
            "id",
            "title",
            "content",
        ]



class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variations = ProductVariationSerializer(many=True, read_only=True)
    sections = ProductDetailSectionSerializer(many=True, read_only=True)

    has_variations = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()
    default_variation = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "short_description",
            "description",

            # 👇 legacy fields (safe)
            "price",
            "offerprice",
            "final_price",

            # 👇 new flow fields
            "has_variations",
            "price_range",
            "default_variation",

            "stock",
            "quantity",
            "unit",
            "is_sku_code",
            "color_code",

            "popular",
            "latest",
            "featured",

            "images",
            "variations",
            "sections",
        ]

    def get_has_variations(self, obj):
        return obj.variations.exists()

    def get_final_price(self, obj):
        """
        Only used if product has NO variations
        """
        if obj.variations.exists():
            return None

        return obj.offerprice if obj.offerprice > 0 else obj.price

    def get_price_range(self, obj):
        variations = obj.variations.all()

        if not variations.exists():
            price = obj.offerprice if obj.offerprice > 0 else obj.price
            return {"min": price, "max": price}

        prices = []
        for v in variations:
            base = obj.price + (v.price_modifier or 0)
            prices.append(v.offerprice if v.offerprice > 0 else base)

        return {
            "min": min(prices),
            "max": max(prices)
        }

    def get_default_variation(self, obj):
        """
        First in-stock variation
        """
        variation = obj.variations.filter(stock__gt=0).order_by("id").first()

        if not variation:
            return None

        return ProductVariationSerializer(
            variation,
            context=self.context
        ).data

