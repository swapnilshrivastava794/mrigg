from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import EmailOTP
from django.utils import timezone
from datetime import timedelta
from ecommerce.models import (
    Category,
    Order,
    OrderItem,
    SubCategory,
    Product,
    ProductImage,
    ProductVariation,
    ProductDetailSection,
    UserAddress,
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
    deal_label = serializers.SerializerMethodField()
    cta_text = serializers.SerializerMethodField()
    redirect = serializers.SerializerMethodField()

    class Meta:
        model = slider
        fields = [
            "id",
            "ad_title",
            "ad_description",
            "image",
            "deal_type",
            "deal_label",
            "cta_text",
            "redirect",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.sliderimage and request:
            return request.build_absolute_uri(obj.sliderimage.url)
        return None

    def get_deal_label(self, obj):
        mapping = {
            "hot_deals": "HOT DEAL",
            "summer_deal": "SUMMER SALE",
            "best_sale_product": "BEST SELLER",
            "high_demand_product": "TRENDING",
        }
        return mapping.get(obj.deal_type, "SPECIAL OFFER")

    def get_cta_text(self, obj):
        return "SHOP NOW"

    def get_redirect(self, obj):
        """
        Frontend ko pata ho:
        - product open karna hai
        - category open karni hai
        """
        if obj.product:
            return {
                "type": "product",
                "id": obj.product.id,
                "slug": obj.product.slug,
            }

        if obj.slidercat:
            return {
                "type": "category",
                "id": obj.slidercat.id,
                "slug": obj.slidercat.slug,
            }

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
        ]



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

    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",                 
            "name",
            "slug",
            "short_description",
            "description",
            "price",
            "offerprice",
            "final_price",
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

    def get_final_price(self, obj):
        return obj.offerprice if obj.offerprice > 0 else obj.price



class ProductSearchListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    has_variants = serializers.SerializerMethodField()
    subcategory = SubCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "image",
            "price",
            "offerprice",
            "final_price",
            "has_variants",
            "subcategory",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        first_image = obj.images.first()
        if first_image and first_image.image:
            return request.build_absolute_uri(first_image.image.url)
        return None

    def get_final_price(self, obj):
        return obj.offerprice if obj.offerprice > 0 else obj.price

    def get_has_variants(self, obj):
        return obj.variations.exists()


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            'id',
            'full_name',
            'phone',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'zip_code',
            'country',
            'is_default'
        ]


class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    items = serializers.ListField(
        child=serializers.DictField()
    )

    def validate_address_id(self, value):
        user = self.context['request'].user
        if not UserAddress.objects.filter(id=value, user=user).exists():
            raise serializers.ValidationError("Invalid address")
        return value
    
class OrderCreateSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    items = serializers.ListField()

    def create(self, validated_data):
        user = self.context['request'].user
        address = UserAddress.objects.get(
            id=validated_data['address_id'],
            user=user
        )

        # 🔒 Address snapshot
        order = Order.objects.create(
            user=user,
            first_name=address.full_name,
            last_name="",
            email=user.email,
            address=f"{address.address_line1}, {address.address_line2 or ''}",
            postal_code=address.zip_code,
            city=address.city
        )

        # 🔒 Cart → OrderItem
        for item in validated_data['items']:
            product = Product.objects.get(id=item['product_id'])
            
            variation = None
            price_to_charge = product.offerprice if product.offerprice > 0 else product.price

            # Check if variation exists
            if 'variation_id' in item and item['variation_id']:
                try:
                    variation = ProductVariation.objects.get(id=item['variation_id'], product=product)
                    # Use variation price if available (assuming variation checks offerprice or price_modifier)
                    # Simple Logic: If variation has offerprice, use it. Else use product price + modifier? 
                    # Let's check model. Variation has offerprice field.
                    if variation.offerprice > 0:
                         price_to_charge = variation.offerprice
                    elif variation.price_modifier:
                         # This logic depends on business requirement. Usually base price + modifier.
                         # But let's stick to what models suggest. Variation has an offerprice field.
                         # Let's assume if variation offerprice is 0, we use product price? No, variation might be just size.
                         # Let's use the safer bet: 
                         # If variation offerprice > 0, use it.
                         # Else if variation price_modifier != 0, add to product price.
                         # For now, let's keep it robust.
                         price_to_charge = product.price + variation.price_modifier
                except ProductVariation.DoesNotExist:
                    variation = None

            OrderItem.objects.create(
                order=order,
                product=product,
                variation=variation,
                price=price_to_charge,
                quantity=item['quantity']
            )

        return order


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    variation_details = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'product_name',
            'variation_details',
            'price',
            'quantity'
        ]

    def get_variation_details(self, obj):
        if obj.variation:
            return {
                "id": obj.variation.id,
                "name": obj.variation.name,
                "quantity": obj.variation.quantity # e.g. XL, Red etc
            }
        return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'created',
            'status',
            'paid',
            'city',
            'items',
            'total_amount'
        ]

    def get_total_amount(self, obj):
        return sum(
            item.price * item.quantity
            for item in obj.items.all()
        )
    
class PaymentSuccessSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

    def validate_order_id(self, value):
        user = self.context['request'].user

        if not Order.objects.filter(id=value, user=user).exists():
            raise serializers.ValidationError("Invalid order ID")

        return value


