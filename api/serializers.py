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
    Coupon,
    CouponUsage,
    Offer,
    OfferProduct,
    Brand,
    CustomUser
)

from cms.models import slider

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser  # 🔥 Fix: Use CustomUser explicitly
        fields = [
            'id',
            'email',
            'username',
            'password',
            'mobile',
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
            'role': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        # Use CustomUser to create user
        user = CustomUser(**validated_data) 
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Safe access for fields that might not exist on default User (admin)
        token['email'] = getattr(user, 'email', '')
        token['role'] = getattr(user, 'role', 'admin') # Default to admin if not found
        token['mobile'] = getattr(user, 'mobile', '')
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Add full user data in response (Safe Access)
        data['user'] = {
            "id": user.id,
            "email": getattr(user, 'email', ''),
            "username": user.username,
            "mobile": getattr(user, 'mobile', ''),
            "role": getattr(user, 'role', 'admin'),
            "first_name": user.first_name,
            "last_name": user.last_name,
            # For optional profile fields, we need to be careful as default User doesn't have them
            "date_of_birth": getattr(user, 'date_of_birth', None),
            "gender": getattr(user, 'gender', None),
            "address_line1": getattr(user, 'address_line1', None),
            "address_line2": getattr(user, 'address_line2', None),
            "city": getattr(user, 'city', None),
            "state": getattr(user, 'state', None),
            "zip_code": getattr(user, 'zip_code', None),
            "country": getattr(user, 'country', None),
            "profile_image": self.context['request'].build_absolute_uri(user.profile_image.url) if getattr(user, 'profile_image', None) else None,
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
    video = serializers.SerializerMethodField()
    media_type = serializers.SerializerMethodField()
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
            "video",
            "video_url",
            "media_type",
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

    def get_video(self, obj):
        request = self.context.get("request")
        if obj.slidervideo and request:
            return request.build_absolute_uri(obj.slidervideo.url)
        return None

    def get_media_type(self, obj):
        return obj.get_media_type()

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




class BrandSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "image", "remark"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variations = ProductVariationSerializer(many=True, read_only=True)
    sections = ProductDetailSectionSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)

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
            "brand",
        ]

    def get_final_price(self, obj):
        return obj.offerprice if obj.offerprice > 0 else obj.price



class ProductSearchListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    has_variants = serializers.SerializerMethodField()
    subcategory = SubCategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

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
            "has_variants",
            "subcategory",
            "brand",
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
    coupon_code = serializers.CharField(required=False, allow_blank=True)

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

    # 🎟️ GLOBAL COUPON LOGIC (Flipkart Style)
        total_order_amount = 0
        order_items_objects = []

        # 1. Create all OrderItems & Calculate Total
        for item_data in validated_data['items']:
            # Use select_related to fetch relationships to avoid "RelatedObjectDoesNotExist"
            try:
                # Optimized fetching, though not strictly needed for simplication, keeps it robust
                product = Product.objects.select_related('subcategory__category').get(id=item_data['product_id'])
            except Product.DoesNotExist:
                 raise serializers.ValidationError(f"Product with ID {item_data['product_id']} does not exist.")
            
            variation = None
            # Default price
            base_price = product.offerprice if product.offerprice > 0 else product.price

            # Check if variation exists
            if 'variation_id' in item_data and item_data['variation_id']:
                try:
                    variation = ProductVariation.objects.get(id=item_data['variation_id'], product=product)
                    if variation.offerprice > 0:
                         base_price = variation.offerprice
                    elif variation.price_modifier:
                         base_price = product.price + variation.price_modifier
                except ProductVariation.DoesNotExist:
                     pass

            quantity = item_data['quantity']
            total_item_price = base_price * quantity
            total_order_amount += total_item_price

            # Create OrderItem
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                variation=variation,
                price=base_price,
                quantity=quantity
            )
            order_items_objects.append({'product': product, 'price': total_item_price})

        # 2. Apply Global Coupon (if provided)
        global_coupon_code = validated_data.get('coupon_code')
        
        if global_coupon_code:
            try:
                coupon = Coupon.objects.get(code=global_coupon_code)
                
                # Simple Global Validation (Active, Dates, Usage Limit, Min Purchase on Total Amount)
                # No Product/Category restrictions checks - Direct Apply
                is_valid, msg = coupon.is_valid(cart_total=float(total_order_amount), user=user)
                
                if not is_valid:
                    raise serializers.ValidationError(f"Coupon error: {msg}")

                # Calculate Discount on Total Order Amount
                discount = coupon.calculate_discount(float(total_order_amount))
                
                # Apply
                order.discount_total = discount
                order.coupon = coupon
                order.coupons.add(coupon)
                order.save()
                
                # Track Usage
                coupon.used_count += 1
                coupon.save()
                CouponUsage.objects.create(user=user, coupon=coupon, order=order)

            except Coupon.DoesNotExist:
                 raise serializers.ValidationError(f"Invalid coupon code: {global_coupon_code}")

        return order

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


class OfferSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField() # Custom image field for absolute URL

    class Meta:
        model = Offer
        fields = [
            'id',
            'offer_name',
            'page_position',
            'offer_title',
            'offer_slug',
            'offer_description',
            'image', # Return 'image' instead of 'offer_image' for consistency
            'meta_title',
            'meta_description',
            'start_date',
            'end_date',
            'products',
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.offer_image and request:
            return request.build_absolute_uri(obj.offer_image.url)
        return None

    def get_products(self, obj):
        # maximize performance by selecting related fields if needed
        offer_products = obj.offer_products.select_related('product').all()
        products = [op.product for op in offer_products]
        # Rewrite context to ensure absolute URLs in nested serializers work
        return ProductSearchListSerializer(products, many=True, context=self.context).data


