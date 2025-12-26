from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import  Group, Permission
from django.db import models

# Try to import AutoSlugField if available
try:
    from autoslug import AutoSlugField
except ImportError:
    AutoSlugField = None

# Try to import AutoSlugField if available
try:
    from autoslug import AutoSlugField
except ImportError:
    AutoSlugField = None



# class CustomUser(AbstractUser):
#     id = models.BigAutoField(primary_key=True)
#     email = models.EmailField(unique=True)
#     mobile = models.CharField(max_length=15, unique=True)

#     first_name = models.CharField(max_length=150, null=True, blank=True)  # Override
#     last_name = models.CharField(max_length=150, null=True, blank=True)   # Override

#     role = models.CharField(
#         max_length=20,
#         choices=[
#             ('customer', 'Customer'),
#             ('admin', 'Admin'),
#             ('support', 'Support Staff'),
#         ],
#         default='customer'
#     )

#     date_of_birth = models.DateField(null=True, blank=True)
#     gender = models.CharField(
#         max_length=10,
#         choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
#         null=True,
#         blank=True
#     )

#     address_line1 = models.CharField(max_length=255, null=True, blank=True)
#     address_line2 = models.CharField(max_length=255, null=True, blank=True)
#     city = models.CharField(max_length=100, null=True, blank=True)
#     state = models.CharField(max_length=100, null=True, blank=True)
#     zip_code = models.CharField(max_length=10, null=True, blank=True)
#     country = models.CharField(max_length=100, null=True, blank=True)

#     profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

#     groups = models.ManyToManyField(
#         Group,
#         related_name='customuser_set',  # avoid clash with auth.User
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='customuser_set',  # avoid clash with auth.User
#         blank=True
#     )

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']  # username is still required by AbstractUser

#     class Meta:
#         db_table = 'main_customuser'  # Use existing table name

#     def __str__(self):
#         return self.email


class CustomUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)

    # 🔐 AUTH
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True)

    # 👤 BASIC INFO (OPTIONAL FOR SIGNUP)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)

    role = models.CharField(
        max_length=20,
        choices=[
            ('customer', 'Customer'),
            ('admin', 'Admin'),
            ('support', 'Support Staff'),
        ],
        default='customer'
    )

    # 👤 OPTIONAL PROFILE INFO
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ],
        null=True,
        blank=True
    )

    # 🏠 OPTIONAL ADDRESS INFO (NOT REQUIRED AT SIGNUP)
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    # 🖼️ PROFILE IMAGE
    profile_image = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )

    # 🔐 PERMISSIONS (Django Admin safe)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True
    )

    # 🔑 LOGIN CONFIG
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # admin compatibility

    class Meta:
        db_table = 'main_customuser'

    def __str__(self):
        return self.email

class Category(models.Model):
    """Main Category (Parent Category) - No parent field"""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d', blank=True, null=True, verbose_name='Category Image')
    is_active = models.BooleanField(default=True, verbose_name="Status")
    order = models.IntegerField(null=True, default=None, verbose_name="Order", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_category'  # Use existing table name
        ordering = ['order', 'name']
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        # Check if this is a new image or if image has changed
        if self.pk:
            try:
                old_instance = Category.objects.get(pk=self.pk)
                old_image = old_instance.image
            except Category.DoesNotExist:
                old_image = None
        else:
            old_image = None
        
        # Save the model first to get the image path
        super(Category, self).save(*args, **kwargs)
        
        # Process image if it exists and is new or changed
        if self.image and (not old_image or self.image != old_image):
            try:
                # Open the image
                img = Image.open(self.image.path)
                
                # Convert RGBA to RGB if necessary (WebP supports transparency, but we'll use RGB for consistency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create a white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Crop and resize to 250x250px (square)
                desired_size = (250, 250)
                
                # Calculate the center crop
                width, height = img.size
                if width > height:
                    # Landscape: crop width
                    left = (width - height) // 2
                    right = left + height
                    top = 0
                    bottom = height
                else:
                    # Portrait or square: crop height
                    top = (height - width) // 2
                    bottom = top + width
                    left = 0
                    right = width
                
                # Crop to square
                img = img.crop((left, top, right, bottom))
                
                # Resize to 250x250
                img = img.resize(desired_size, Image.Resampling.LANCZOS)
                
                # Get the file path and change extension to .webp
                file_path = self.image.path
                base_path = os.path.splitext(file_path)[0]
                webp_path = base_path + '.webp'
                
                # Save as WebP
                img.save(webp_path, 'WEBP', quality=85, optimize=True)
                
                # Update the image field to point to the WebP file
                # Get the relative path from MEDIA_ROOT
                media_root = str(settings.MEDIA_ROOT)
                relative_path = os.path.relpath(webp_path, media_root)
                self.image.name = relative_path.replace('\\', '/')
                
                # Delete the original file if it's not WebP
                if not file_path.lower().endswith('.webp') and os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass
                
                # Save again to update the image field
                super(Category, self).save(update_fields=['image'])
                
            except Exception as e:
                # If image processing fails, continue without processing
                print(f"Error processing category image: {e}")
                pass

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """SubCategory (Child Category) - Linked to Category via ForeignKey"""
    id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Main Category'
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='subcategories/%Y/%m/%d', blank=True, null=True, verbose_name='SubCategory Image')
    is_active = models.BooleanField(default=True, verbose_name="Status")
    order = models.IntegerField(null=True, default=None, verbose_name="Order", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_subcategory'  # New table name
        ordering = ['category__order', 'category__name', 'order', 'name']
        verbose_name_plural = 'SubCategories'
        unique_together = ('category', 'slug')  # Slug should be unique per category

    def save(self, *args, **kwargs):
        # Check if this is a new image or if image has changed
        if self.pk:
            try:
                old_instance = SubCategory.objects.get(pk=self.pk)
                old_image = old_instance.image
            except SubCategory.DoesNotExist:
                old_image = None
        else:
            old_image = None
        
        # Save the model first to get the image path
        super(SubCategory, self).save(*args, **kwargs)
        
        # Process image if it exists and is new or changed
        if self.image and (not old_image or self.image != old_image):
            try:
                # Open the image
                img = Image.open(self.image.path)
                
                # Convert RGBA to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Crop and resize to 250x250px (square)
                desired_size = (250, 250)
                width, height = img.size
                if width > height:
                    left = (width - height) // 2
                    right = left + height
                    top = 0
                    bottom = height
                else:
                    top = (height - width) // 2
                    bottom = top + width
                    left = 0
                    right = width
                
                img = img.crop((left, top, right, bottom))
                img = img.resize(desired_size, Image.Resampling.LANCZOS)
                
                # Get the file path and change extension to .webp
                file_path = self.image.path
                base_path = os.path.splitext(file_path)[0]
                webp_path = base_path + '.webp'
                
                # Save as WebP
                img.save(webp_path, 'WEBP', quality=85, optimize=True)
                
                # Update the image field
                media_root = str(settings.MEDIA_ROOT)
                relative_path = os.path.relpath(webp_path, media_root)
                self.image.name = relative_path.replace('\\', '/')
                
                # Delete the original file if it's not WebP
                if not file_path.lower().endswith('.webp') and os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass
                
                # Save again to update the image field
                super(SubCategory, self).save(update_fields=['image'])
                
            except Exception as e:
                print(f"Error processing subcategory image: {e}")
                pass

    def __str__(self):
        return f"{self.category.name} / {self.name}"


class Brand(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='brands/%Y/%m/%d', blank=True, null=True, verbose_name='Brand Image')
    remark = models.TextField(blank=True, null=True, verbose_name='Remark/Description')
    is_active = models.BooleanField(default=True, verbose_name="Status")
    order = models.IntegerField(null=True, default=None, verbose_name="Order", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_brand'  # Use existing table name
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        # Check if this is a new image or if image has changed
        if self.pk:
            try:
                old_instance = Brand.objects.get(pk=self.pk)
                old_image = old_instance.image
            except Brand.DoesNotExist:
                old_image = None
        else:
            old_image = None
        
        # Save the model first to get the image path
        super(Brand, self).save(*args, **kwargs)
        
        # Process image if it exists and is new or changed
        if self.image and (not old_image or self.image != old_image):
            try:
                # Open the image
                img = Image.open(self.image.path)
                
                # Convert RGBA to RGB if necessary (WebP supports transparency, but we'll use RGB for consistency)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create a white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Crop and resize to 250x250px (square)
                desired_size = (250, 250)
                
                # Calculate the center crop
                width, height = img.size
                if width > height:
                    # Landscape: crop width
                    left = (width - height) // 2
                    right = left + height
                    top = 0
                    bottom = height
                else:
                    # Portrait or square: crop height
                    top = (height - width) // 2
                    bottom = top + width
                    left = 0
                    right = width
                
                # Crop to square
                img = img.crop((left, top, right, bottom))
                
                # Resize to 250x250
                img = img.resize(desired_size, Image.Resampling.LANCZOS)
                
                # Get the file path and change extension to .webp
                file_path = self.image.path
                base_path = os.path.splitext(file_path)[0]
                webp_path = base_path + '.webp'
                
                # Save as WebP
                img.save(webp_path, 'WEBP', quality=85, optimize=True)
                
                # Update the image field to point to the WebP file
                # Get the relative path from MEDIA_ROOT
                media_root = str(settings.MEDIA_ROOT)
                relative_path = os.path.relpath(webp_path, media_root)
                self.image.name = relative_path.replace('\\', '/')
                
                # Delete the original file if it's not WebP
                if not file_path.lower().endswith('.webp') and os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass
                
                # Save again to update the image field
                super(Brand, self).save(update_fields=['image'])
                
            except Exception as e:
                # If image processing fails, continue without processing
                print(f"Error processing brand image: {e}")
                pass

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('ml', 'ml'),
        ('l', 'L'),
        ('g', 'g'),
        ('kg', 'kg'),
        ('pcs', 'pcs'),
        ('pieces', 'pieces'),
        ('m', 'm'),
        ('cm', 'cm'),
        ('inch', 'inch'),
        ('ft', 'ft'),
        ('oz', 'oz'),
        ('lb', 'lb'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    subcategory = models.ForeignKey('SubCategory', related_name='products', on_delete=models.CASCADE, verbose_name='SubCategory')
    brand = models.ForeignKey('Brand', related_name='products', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Brand')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300, blank=True)  # ✅ added short description
    description = models.TextField(verbose_name="Key Points")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='MRP (INR)')
    offerprice = models.DecimalField(max_digits=10, decimal_places=2, default='00.00', verbose_name='Offer Price (INR)')
    stock = models.PositiveIntegerField()
    quantity = models.CharField(max_length=100, blank=True, null=True, verbose_name='Qty')
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, blank=True, null=True, verbose_name='Unit')
    is_sku_code = models.CharField(max_length=100, blank=True, null=True, verbose_name='SKU Code')
    color_code = models.CharField(max_length=7, blank=True, null=True, verbose_name='Color Code')
    popular=models.BooleanField(default=True)
    latest=models.BooleanField(default=True)
    featured=models.BooleanField(default=True)
    available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, verbose_name="Status")
    order=models.IntegerField(null=True,default=None,verbose_name="Order", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_product'  # Use existing table name

    def __str__(self):
        return self.name
    

class ProductVariation(models.Model):
    UNIT_CHOICES = [
        ('ml', 'ml'),
        ('l', 'L'),
        ('g', 'g'),
        ('kg', 'kg'),
        ('pcs', 'pcs'),
        ('pieces', 'pieces'),
        ('m', 'm'),
        ('cm', 'cm'),
        ('inch', 'inch'),
        ('ft', 'ft'),
        ('oz', 'oz'),
        ('lb', 'lb'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Name')  # e.g., 'Size' or 'Color'
    quantity = models.CharField(max_length=100, blank=True, null=True, verbose_name='Qty')  # e.g., 'Large' or 'Red'
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, blank=True, null=True, verbose_name='Unit')  # e.g., 'ml', 'kg', 'pcs'
    is_sku_code = models.CharField(max_length=100, blank=True, null=True, verbose_name='SKU Code')
    color_code = models.CharField(max_length=7, blank=True, null=True, verbose_name='Color Code')
    # Slug field - will be auto-populated from name in save() method
    slug = models.SlugField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Slug'
    )
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True, verbose_name='Price +/-')
    offerprice = models.DecimalField(max_digits=10, decimal_places=2, default='00.00', blank=True, null=True, verbose_name='Offer Price (INR)')
    stock = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Stock')

    class Meta:
        db_table = 'main_productvariation'  # Use existing table name
        unique_together = ('product', 'name', 'quantity')

    def save(self, *args, **kwargs):
        # Ensure product is saved first
        if self.product and not self.product.pk:
            self.product.save()
        
        # Generate slug from name if name exists and slug is empty or needs update
        if self.name:
            from django.utils.text import slugify
            base_slug = slugify(self.name)
            
            # Update slug if empty, None, or doesn't match name
            if not self.slug or (isinstance(self.slug, str) and self.slug.strip() == '') or self.slug != base_slug:
                self.slug = base_slug
                
                # Ensure uniqueness within the product
                if self.product and self.product.pk:
                    counter = 1
                    original_slug = self.slug
                    while ProductVariation.objects.filter(
                        product=self.product, slug=self.slug
                    ).exclude(id=self.id if self.id else None).exists():
                        self.slug = f"{original_slug}-{counter}"
                        counter += 1
                        # Prevent infinite loop
                        if counter > 1000:
                            break
        
        # Call parent save
        super().save(*args, **kwargs)

    def clean(self):
        # This ensures no duplicate variation (like Size=25, Color=Red) for the same product
        # Only validate if product is saved (has a primary key)
        if self.product and self.product.pk:
            if ProductVariation.objects.filter(
                product=self.product, name=self.name, quantity=self.quantity
            ).exclude(id=self.id).exists():
                raise ValidationError(f"This variation '{self.name}: {self.quantity}' already exists for this product.")

    def __str__(self):
        # Simplified string for admin display to prevent overlap
        if self.quantity:
            return f"{self.name}: {self.quantity}"
        return f"{self.name}" if self.name else "Variation"
    
class ProductDetailSection(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)  # Example: 'Information', 'Cart Details', 'Shipping & Returns'
    content = models.TextField()

    class Meta:
        db_table = 'main_productdetailsection'  # Use existing table name

    def __str__(self):
        return f"{self.product.name} - {self.title}"


class ProductImage(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES,
        default='image',
        verbose_name='Media Type'
    )
    alt_text = models.CharField(max_length=255, blank=True)
    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True,
        null=True,
        help_text='Upload image or video file (for video, max 2MB)'
    )
    
    class Meta:
        db_table = 'main_productimage'  # Use existing table name
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Validate video file size if media type is video (2MB = 2 * 1024 * 1024 bytes)
        if self.media_type == 'video' and self.image:
            if self.image.size > 2 * 1024 * 1024:
                raise ValidationError({'image': 'Video file size must be less than 2MB.'})
    
    def save(self, *args, **kwargs):
        # Override the save method to resize the image before saving (only for images)
        super(ProductImage, self).save(*args, **kwargs)
        
        # Process image if media type is image
        if self.media_type == 'image' and self.image:
            try:
                # Open the image
                img = Image.open(self.image.path)
                # Set the desired size for cropping (width, height)
                desired_size = (1080, 1080)
                # Resize the image while maintaining the aspect ratio
                img.thumbnail(desired_size)
                # Save the resized image back to the original path
                img.save(self.image.path)
            except Exception as e:
                print(f"Error processing product image: {e}")
    
    def __str__(self):
        media_type_display = self.get_media_type_display()
        return f"{media_type_display} for {self.product.name}"
    

class Order(models.Model):
    ORDER_STATUS = (
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='created'
    )

    class Meta:
        db_table = 'main_order'  # Use existing table name

    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariation, related_name='order_items', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'main_orderitem'  # Use existing table name

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'


class UserAddress(models.Model):
    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        CustomUser,
        related_name='addresses',
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    is_default = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_useraddress'
        ordering = ['-is_default', '-updated']

    def __str__(self):
        return f"{self.full_name} - {self.city}"




class ContactMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'main_contactmessage'  # Use existing table name

    def __str__(self):
        return f"{self.name} - {self.email}"
    

# //Custom User Model



