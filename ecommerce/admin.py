from django.contrib import admin
from .models import Brand, Category, SubCategory, ContactMessage, CustomUser, Product, Order, OrderItem, ProductDetailSection ,ProductImage, ProductVariation, Coupon, CouponUsage
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from django import forms
import logging
import time
from django.db import connection, reset_queries

# Setup logger
logger = logging.getLogger('ecommerce.admin')


# ==================== ORDER: 1. Brand ====================
class BrandAdminForm(forms.ModelForm):
    remark = forms.CharField(widget=CKEditorWidget(config_name='default'), required=False)
    
    class Meta:
        model = Brand
        fields = '__all__'

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    form = BrandAdminForm
    list_display = ('name', 'slug', 'image', 'is_active', 'order', 'created', 'updated')
    list_filter = ('is_active', 'created', 'updated')
    search_fields = ('name', 'remark')
    ordering = ('order', 'name')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')
    list_per_page = 30
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'image', 'remark')
        }),
        ('Status & Ordering', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created', 'updated')


# ==================== ORDER: 2. Category ====================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image', 'is_active', 'order', 'created', 'updated')
    list_filter = ('is_active', 'created', 'updated')
    search_fields = ('name',)
    ordering = ('order', 'name')
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug from name
    list_editable = ('is_active', 'order')
    list_per_page = 30
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'image')
        }),
        ('Status & Ordering', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created', 'updated')


# ==================== ORDER: 3. SubCategory ====================
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_category', 'slug', 'image', 'is_active', 'order', 'created', 'updated')
    list_filter = ('is_active', 'category', 'created', 'updated')
    search_fields = ('name', 'category__name')
    ordering = ('category__order', 'category__name', 'order', 'name')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')
    list_per_page = 30
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'image')
        }),
        ('Status & Ordering', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created', 'updated')
    
    def get_category(self, obj):
        """Display parent category name"""
        return obj.category.name if obj.category else '-'
    get_category.short_description = 'Category'
    get_category.admin_order_field = 'category__name'
    
    def get_queryset(self, request):
        """Optimize queryset to avoid N+1 queries"""
        qs = super().get_queryset(request)
        return qs.select_related('category')


# ProductImageInline and ProductSectionInline removed - now managed separately

class ProductVariationInlineForm(forms.ModelForm):
    name = forms.CharField(required=False, max_length=100, label='Name')
    quantity = forms.CharField(required=False, max_length=100, label='Qty')
    unit = forms.ChoiceField(required=False, choices=ProductVariation.UNIT_CHOICES, label='Unit')
    color_code = forms.CharField(
        required=False,
        label='Color Code',
        widget=forms.TextInput(attrs={'type': 'color', 'style': 'width: 80px; height: 35px;'})
    )
    is_sku_code = forms.CharField(
        required=False,
        label='SKU Code',
        max_length=100
    )
    price_modifier = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Price +/-')
    offerprice = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Offer Price (INR)')
    stock = forms.IntegerField(required=False, label='Stock')
    
    class Meta:
        model = ProductVariation
        fields = '__all__'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Generate slug from name if name exists
        if instance.name:
            from django.utils.text import slugify
            base_slug = slugify(instance.name)
            instance.slug = base_slug
            
            # Ensure uniqueness within the product
            if instance.product and instance.product.pk:
                counter = 1
                original_slug = instance.slug
                while ProductVariation.objects.filter(
                    product=instance.product, slug=instance.slug
                ).exclude(id=instance.id if instance.id else None).exists():
                    instance.slug = f"{original_slug}-{counter}"
                    counter += 1
        
        if commit:
            instance.save()
        return instance

class ProductVariationInline(admin.TabularInline):
    form = ProductVariationInlineForm
    model = ProductVariation
    extra = 1
    can_delete = True
    fields = ('name', 'is_sku_code', 'quantity', 'unit', 'color_code', 'price_modifier', 'offerprice', 'stock')
    verbose_name = 'Variation'
    verbose_name_plural = 'Variations'
    max_num = 20  # Limit number of rows
    show_change_link = False  # Hide change link to save space

class ProductSectionInlineForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='default'), required=False)
    
    class Meta:
        model = ProductDetailSection
        fields = '__all__'


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(config_name='default'), required=False)
    color_code = forms.CharField(
        required=False,
        label='Color Code',
        widget=forms.TextInput(attrs={'type': 'color', 'style': 'width: 80px; height: 35px;'})
    )
    
    class Meta:
        model = Product
        fields = '__all__'

# ==================== ORDER: 4. Product ====================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'get_category', 'get_subcategory', 'price','offerprice','popular','latest','featured', 'stock', 'available', 'action_buttons', 'created', 'updated']
    # Simplified list_filter - use subcategory and brand
    list_filter = ['available', 'created', 'updated', 'subcategory', 'subcategory__category', 'brand']
    search_fields = ['name', 'slug', 'short_description']  # Required for autocomplete in ProductVariation
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 50  # Limit items per page to reduce load
    show_full_result_count = False  # Disable full count for faster loading
    # ProductImage and ProductDetailSection removed from inline - now managed separately
    
    def changelist_view(self, request, extra_context=None):
        """Override changelist_view to add performance logging"""
        start_time = time.time()
        reset_queries()
        
        logger.info(f"=== ProductAdmin changelist_view started ===")
        logger.info(f"Request path: {request.path}")
        logger.info(f"Request GET params: {request.GET}")
        logger.info(f"User: {request.user}")
        
        try:
            # Get queryset and log info
            qs = self.get_queryset(request)
            
            # Use exists() instead of count() for faster check
            start_count = time.time()
            total_count = qs.count()
            count_time = time.time() - start_count
            logger.info(f"Total products in queryset: {total_count} (count took {count_time:.3f}s)")
            
            if count_time > 1:
                logger.warning(f"WARNING: Count query took {count_time:.3f}s - this is slow!")
            
            # Log query count before rendering
            query_count_before = len(connection.queries)
            logger.info(f"Database queries before rendering: {query_count_before}")
            
            # Log all queries so far
            if query_count_before > 0:
                logger.debug("Queries executed so far:")
                for i, query in enumerate(connection.queries, 1):
                    logger.debug(f"  Query {i}: {query['sql'][:150]}... (Time: {query['time']}s)")
            
            # Log time before calling parent
            time_before_super = time.time()
            logger.info(f"About to call super().changelist_view() at {time_before_super:.3f}")
            
            # Call parent method
            try:
                response = super().changelist_view(request, extra_context)
                time_after_super = time.time()
                logger.info(f"super().changelist_view() completed in {time_after_super - time_before_super:.3f}s")
            except Exception as e:
                time_after_super = time.time()
                logger.error(f"ERROR in super().changelist_view() after {time_after_super - time_before_super:.3f}s: {str(e)}", exc_info=True)
                raise
            
            # Log query count after rendering
            query_count_after = len(connection.queries)
            total_queries = query_count_after - query_count_before
            elapsed_time = time.time() - start_time
            
            logger.info(f"Database queries after rendering: {query_count_after}")
            logger.info(f"Total queries executed: {total_queries}")
            logger.info(f"Time taken: {elapsed_time:.2f} seconds")
            
            # Log all queries if too many
            if total_queries > 10:
                logger.warning(f"WARNING: Too many queries ({total_queries})!")
                for i, query in enumerate(connection.queries[query_count_before:], 1):
                    logger.debug(f"Query {i}: {query['sql'][:200]}... (Time: {query['time']}s)")
            
            if elapsed_time > 5:
                logger.error(f"ERROR: Request took too long ({elapsed_time:.2f}s)!")
            
            logger.info(f"=== ProductAdmin changelist_view completed ===")
            
            return response
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"ERROR in changelist_view after {elapsed_time:.2f}s: {str(e)}", exc_info=True)
            raise
    
    def get_queryset(self, request):
        """Optimize queryset to avoid N+1 queries"""
        start_time = time.time()
        logger.info("get_queryset called")
        
        qs = super().get_queryset(request)
        
        # Log initial queryset info
        initial_count = qs.count()
        logger.info(f"Initial queryset count: {initial_count}")
        
        # Select related for direct foreign keys including subcategory and its category
        # Order by ID descending for faster pagination
        qs = qs.select_related('subcategory', 'subcategory__category', 'brand').order_by('-id')
        
        elapsed = time.time() - start_time
        logger.info(f"get_queryset completed in {elapsed:.3f}s")
        
        return qs
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Override to filter subcategory choices"""
        if db_field.name == 'subcategory':
            try:
                # Show only active subcategories with their category
                kwargs['queryset'] = SubCategory.objects.filter(
                    is_active=True
                ).select_related('category').order_by('category__order', 'category__name', 'order', 'name')
            except Exception:
                # Fallback to all active subcategories if there's an issue
                kwargs['queryset'] = SubCategory.objects.filter(is_active=True).select_related('category').order_by('order', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_category(self, obj):
        """Display parent category (main category)"""
        try:
            if obj.subcategory and obj.subcategory.category:
                return obj.subcategory.category.name
        except (AttributeError, Exception):
            pass
        return '-'
    get_category.short_description = 'Category'
    get_category.admin_order_field = 'subcategory__category__name'
    
    def get_subcategory(self, obj):
        """Display subcategory"""
        try:
            if obj.subcategory:
                return obj.subcategory.name
        except (AttributeError, Exception):
            pass
        return '-'
    get_subcategory.short_description = 'SubCategory'
    get_subcategory.admin_order_field = 'subcategory__name'
    
    def action_buttons(self, obj):
        """Display action buttons for Add Image, Add Variation, Add Details"""
        from django.utils.html import format_html
        from django.urls import reverse
        
        if not obj or not obj.pk:
            return '-'
        
        # URLs for add pages with product pre-selected
        add_image_url = reverse('admin:ecommerce_productimage_add') + f'?product={obj.pk}'
        add_variation_url = reverse('admin:ecommerce_productvariation_add') + f'?product={obj.pk}'
        add_details_url = reverse('admin:ecommerce_productdetailsection_add') + f'?product={obj.pk}'
        
        buttons = format_html(
            '<div style="white-space: nowrap;">'
            '<a href="{}" class="button" style="margin-right: 5px; padding: 5px 10px; background: #417690; color: white; text-decoration: none; border-radius: 3px; font-size: 11px;">Add Image</a> '
            '<a href="{}" class="button" style="margin-right: 5px; padding: 5px 10px; background: #417690; color: white; text-decoration: none; border-radius: 3px; font-size: 11px;">Add Variation</a> '
            '<a href="{}" class="button" style="padding: 5px 10px; background: #417690; color: white; text-decoration: none; border-radius: 3px; font-size: 11px;">Add Details</a>'
            '</div>',
            add_image_url,
            add_variation_url,
            add_details_url
        )
        return buttons
    action_buttons.short_description = 'Actions'
    action_buttons.allow_tags = True

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    
    def get_queryset(self, request):
        """Optimize queryset for inline"""
        qs = super().get_queryset(request)
        return qs.select_related('product')

# ==================== ORDER: 5. Order ====================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    
    def get_queryset(self, request):
        """Optimize queryset to avoid N+1 queries"""
        qs = super().get_queryset(request)
        return qs.select_related('user')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'mobile', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'mobile')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'mobile')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Address'), {
            'fields': (
                'address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country'
            )
        }),
        (_('Roles & Status'), {'fields': ('role',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'mobile', 'role', 'password1', 'password2'),
        }),
    )


# ==================== Product Variation Admin (Separate) ====================
class ProductVariationAdminForm(forms.ModelForm):
    """Custom form for ProductVariation"""
    name = forms.CharField(required=False, max_length=100, label='Name')
    quantity = forms.CharField(required=False, max_length=100, label='Qty')
    unit = forms.ChoiceField(required=False, choices=ProductVariation.UNIT_CHOICES, label='Unit')
    color_code = forms.CharField(
        required=False,
        label='Color Code',
        widget=forms.TextInput(attrs={'type': 'color', 'style': 'width: 80px; height: 35px;'})
    )
    is_sku_code = forms.CharField(
        required=False,
        label='SKU Code',
        max_length=100
    )
    price_modifier = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Price +/-')
    offerprice = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label='Offer Price (INR)')
    stock = forms.IntegerField(required=False, label='Stock')
    slug = forms.SlugField(
        required=False,
        max_length=200,
        label='Slug',
        help_text='Auto-generated from name. You can edit it manually if needed.',
        widget=forms.TextInput(attrs={'style': 'background-color: #f8f9fa;'})
    )
    
    class Meta:
        model = ProductVariation
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Auto-populate slug from name if name exists and slug is empty
        if self.instance and self.instance.pk:
            # Existing instance - populate slug if empty
            if not self.instance.slug and self.instance.name:
                from django.utils.text import slugify
                self.instance.slug = slugify(self.instance.name)
                self.initial['slug'] = self.instance.slug
        elif self.data and 'name' in self.data and self.data.get('name'):
            # New instance - generate slug from name
            from django.utils.text import slugify
            name = self.data.get('name')
            if name:
                slug_value = slugify(name)
                self.initial['slug'] = slug_value
    
    def clean(self):
        cleaned_data = super().clean()
        # Ensure slug is generated from name if it's empty
        name = cleaned_data.get('name')
        slug = cleaned_data.get('slug')
        
        if name and (not slug or (isinstance(slug, str) and slug.strip() == '')):
            from django.utils.text import slugify
            cleaned_data['slug'] = slugify(name)
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Ensure product is saved first
        if instance.product and not instance.product.pk:
            instance.product.save()
        
        # ALWAYS generate slug from name if name exists (even if slug is already set)
        if instance.name:
            from django.utils.text import slugify
            base_slug = slugify(instance.name)
            
            # Only update if slug is empty or doesn't match the name-based slug
            # This allows manual edits but auto-generates if empty
            if not instance.slug or (instance.slug and instance.slug.strip() == ''):
                instance.slug = base_slug
            elif instance.slug != base_slug:
                # If slug exists but doesn't match name, update it (name was changed)
                instance.slug = base_slug
            
            # Ensure uniqueness within the product (only if product exists)
            if instance.product and instance.product.pk:
                counter = 1
                original_slug = instance.slug
                # Check for duplicates excluding current instance
                while ProductVariation.objects.filter(
                    product=instance.product, 
                    slug=instance.slug
                ).exclude(id=instance.id if instance.id else None).exists():
                    instance.slug = f"{original_slug}-{counter}"
                    counter += 1
                    # Prevent infinite loop
                    if counter > 1000:
                        break
        
        if commit:
            # Save the instance - this will call the model's save() method
            # but our slug is already set, so it should work
            instance.save()
        return instance

@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    form = ProductVariationAdminForm
    list_display = ('get_product_name', 'name', 'quantity', 'unit', 'is_sku_code', 'price_modifier', 'offerprice', 'stock', 'color_code', 'slug')
    list_filter = ('product', 'unit', 'product__subcategory', 'product__brand')
    search_fields = ('product__name', 'name', 'quantity', 'is_sku_code', 'slug')
    list_editable = ('price_modifier', 'offerprice', 'stock')
    list_per_page = 50
    autocomplete_fields = ('product',)  # Use autocomplete for better UX - requires search_fields in ProductAdmin
    readonly_fields = ()  # Slug will be handled by form widget
    
    class Media:
        js = ('admin/js/product_variation_admin.js',)
    
    def get_initial(self, request):
        """Pre-select product from query string"""
        initial = super().get_initial(request)
        product_id = request.GET.get('product')
        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                initial['product'] = product.pk
            except Product.DoesNotExist:
                pass
        return initial
    
    fieldsets = (
        ('Product Information', {
            'fields': ('product',),
            'description': 'Select the product this variation belongs to. Use autocomplete to search by product name.'
        }),
        ('Variation Details', {
            'fields': ('name', 'quantity', 'unit', 'slug'),
            'description': 'Slug is auto-generated from name. Leave blank to auto-generate.'
        }),
        ('SKU & Color', {
            'fields': ('is_sku_code', 'color_code')
        }),
        ('Pricing & Stock', {
            'fields': ('price_modifier', 'offerprice', 'stock')
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset to avoid N+1 queries"""
        qs = super().get_queryset(request)
        return qs.select_related('product', 'product__subcategory', 'product__brand')
    
    def get_product_name(self, obj):
        """Display product name with link to product admin page"""
        if obj.product:
            from django.utils.html import format_html
            from django.urls import reverse
            url = reverse('admin:ecommerce_product_change', args=[obj.product.pk])
            return format_html('<a href="{}">{}</a>', url, obj.product.name)
        return '-'
    get_product_name.short_description = 'Product'
    get_product_name.admin_order_field = 'product__name'


# ==================== Product Image Admin (Separate with Bulk Upload) ====================
class BulkProductImageForm(forms.ModelForm):
    """Form for bulk upload - 3 mandatory images, 1 optional image, 1 optional video"""
    
    # Multiple image fields (first 3 are mandatory, 4th is optional)
    image_1 = forms.ImageField(required=True, label='Image 1 *', help_text='Required')
    image_2 = forms.ImageField(required=True, label='Image 2 *', help_text='Required')
    image_3 = forms.ImageField(required=True, label='Image 3 *', help_text='Required')
    image_4 = forms.ImageField(required=False, label='Image 4 (Optional)', help_text='Optional')
    
    # Video field (1 video - optional)
    video = forms.FileField(
        required=False,
        label='Video (Optional - max 2MB)',
        help_text='Upload video file (max 2MB) - Optional'
    )
    
    # Alt texts for images
    alt_text_1 = forms.CharField(required=False, max_length=255, label='Alt Text 1')
    alt_text_2 = forms.CharField(required=False, max_length=255, label='Alt Text 2')
    alt_text_3 = forms.CharField(required=False, max_length=255, label='Alt Text 3')
    alt_text_4 = forms.CharField(required=False, max_length=255, label='Alt Text 4')
    video_alt_text = forms.CharField(required=False, max_length=255, label='Video Alt Text')
    
    class Meta:
        model = ProductImage
        fields = ['product']  # Product field from model
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure product field is visible - widget will be set by formfield_for_foreignkey
        if 'product' in self.fields:
            self.fields['product'].required = True
            self.fields['product'].label = 'Product'
            self.fields['product'].help_text = 'Select the product for these media files. You can search by typing product name.'
    
    def clean(self):
        cleaned_data = super().clean()
        # First 3 images are mandatory (already validated by required=True)
        # 4th image and video are optional
        video = cleaned_data.get('video')
        
        # Validate video size if provided
        if video:
            if video.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError({'video': 'Video file size must be less than 2MB.'})
        
        return cleaned_data
    
    def save(self, commit=True):
        # This form doesn't save directly, it's handled in add_view
        return None

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('get_product_name', 'media_type', 'alt_text', 'get_preview')
    list_filter = ('media_type', 'product', 'product__subcategory', 'product__brand')
    search_fields = ('product__name', 'alt_text')
    list_editable = ('media_type',)
    list_per_page = 50
    autocomplete_fields = ('product',)  # Use autocomplete for better UX
    
    def get_form(self, request, obj=None, **kwargs):
        """Use bulk form for add, regular form for change"""
        if obj is None:  # Adding new
            # Get the form class
            form_class = BulkProductImageForm
            # Apply formfield_for_foreignkey to set autocomplete widget
            # We need to modify the form's base_fields
            product_field = ProductImage._meta.get_field('product')
            if 'product' in form_class.base_fields:
                # Get the formfield using formfield_for_foreignkey
                formfield = self.formfield_for_foreignkey(product_field, request)
                form_class.base_fields['product'] = formfield
            return form_class
        return super().get_form(request, obj, **kwargs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Set autocomplete widget for product field with search"""
        if db_field.name == 'product':
            # Use autocomplete with search functionality
            # Pass the field itself, not remote_field
            kwargs['widget'] = admin.widgets.AutocompleteSelect(
                db_field,
                admin.site
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_fieldsets(self, request, obj=None):
        """Different fieldsets for add vs change"""
        if obj is None:  # Adding new - use bulk form fieldsets
            return (
                ('Product Information', {
                    'fields': ('product',),
                    'description': 'Select the product for these media files.'
                }),
                ('Images (First 3 are mandatory, 4th is optional)', {
                    'fields': (
                        ('image_1', 'alt_text_1'),
                        ('image_2', 'alt_text_2'),
                        ('image_3', 'alt_text_3'),
                        ('image_4', 'alt_text_4'),
                    ),
                    'description': 'Upload 3 mandatory images (Image 1, 2, 3) and 1 optional image (Image 4).'
                }),
                ('Video (Optional - max 2MB)', {
                    'fields': ('video', 'video_alt_text'),
                    'description': 'Upload one video file (max 2MB) for this product. Video is optional.'
                }),
            )
        else:  # Editing existing - use regular fieldsets
            return (
                ('Product Information', {
                    'fields': ('product',),
                    'description': 'Select the product this media belongs to. Use autocomplete to search by product name.'
                }),
                ('Media Content', {
                    'fields': ('media_type', 'image', 'alt_text'),
                    'description': 'Select media type (Image/Video) and upload file. For video, max 2MB. Both use the same field.'
                }),
            )
    
    def add_view(self, request, form_url='', extra_context=None):
        """Override add_view to handle bulk upload and pre-select product from query string"""
        # Pre-select product from query string if provided
        product_id = request.GET.get('product')
        initial_data = {}
        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                initial_data['product'] = product.pk
            except Product.DoesNotExist:
                pass
        
        if request.method == 'POST':
            form = BulkProductImageForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.cleaned_data['product']
                created_count = 0
                
                # Create ProductImage objects for images
                for i in range(1, 5):
                    image = form.cleaned_data.get(f'image_{i}')
                    alt_text = form.cleaned_data.get(f'alt_text_{i}', '')
                    
                    if image:
                        ProductImage.objects.create(
                            product=product,
                            media_type='image',
                            image=image,
                            alt_text=alt_text
                        )
                        created_count += 1
                
                # Create ProductImage object for video
                video = form.cleaned_data.get('video')
                if video:
                    video_alt_text = form.cleaned_data.get('video_alt_text', '')
                    ProductImage.objects.create(
                        product=product,
                        media_type='video',
                        image=video,  # Using image field for video too
                        alt_text=video_alt_text
                    )
                    created_count += 1
                
                if created_count > 0:
                    from django.contrib import messages
                    messages.success(request, f'Successfully created {created_count} media item(s).')
                    from django.shortcuts import redirect
                    from django.urls import reverse
                    return redirect(reverse('admin:ecommerce_productimage_changelist'))
                else:
                    form.add_error(None, 'No files were uploaded.')
        else:
            form = BulkProductImageForm(initial=initial_data)
        
        # Use default admin add view with custom form
        return super().add_view(request, form_url, extra_context)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Use regular form for editing existing items"""
        return super().change_view(request, object_id, form_url, extra_context)
    
    def get_queryset(self, request):
        """Optimize queryset to avoid N+1 queries"""
        qs = super().get_queryset(request)
        return qs.select_related('product', 'product__subcategory', 'product__brand')
    
    def get_product_name(self, obj):
        """Display product name with link"""
        if obj.product:
            from django.utils.html import format_html
            from django.urls import reverse
            url = reverse('admin:ecommerce_product_change', args=[obj.product.pk])
            return format_html('<a href="{}">{}</a>', url, obj.product.name)
        return '-'
    get_product_name.short_description = 'Product'
    get_product_name.admin_order_field = 'product__name'
    
    def get_preview(self, obj):
        """Display preview of image or video"""
        from django.utils.html import format_html
        if obj.image:
            if obj.media_type == 'video':
                return format_html('<video src="{}" style="max-width: 100px; max-height: 100px;" controls></video>', obj.image.url)
            else:
                return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image.url)
        return '-'
    get_preview.short_description = 'Preview'


# ==================== Product Detail Section Admin (Separate) ====================
@admin.register(ProductDetailSection)
class ProductDetailSectionAdmin(admin.ModelAdmin):
    form = ProductSectionInlineForm  # Reuse the existing form
    list_display = ('get_product_name', 'title', 'get_content_preview')
    list_filter = ('product', 'product__subcategory', 'product__brand')
    search_fields = ('product__name', 'title', 'content')
    list_per_page = 50
    autocomplete_fields = ('product',)  # Use autocomplete for better UX
    
    def get_initial(self, request):
        """Pre-select product from query string"""
        initial = super().get_initial(request)
        product_id = request.GET.get('product')
        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                initial['product'] = product.pk
            except Product.DoesNotExist:
                pass
        return initial
    
    fieldsets = (
        ('Product Information', {
            'fields': ('product',),
            'description': 'Select the product this section belongs to. Use autocomplete to search by product name.'
        }),
        ('Section Content', {
            'fields': ('title', 'content')
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset to avoid N+1 queries"""
        qs = super().get_queryset(request)
        return qs.select_related('product', 'product__subcategory', 'product__brand')
    
    def get_product_name(self, obj):
        """Display product name with link"""
        if obj.product:
            from django.utils.html import format_html
            from django.urls import reverse
            url = reverse('admin:ecommerce_product_change', args=[obj.product.pk])
            return format_html('<a href="{}">{}</a>', url, obj.product.name)
        return '-'
    get_product_name.short_description = 'Product'
    get_product_name.admin_order_field = 'product__name'
    
    def get_content_preview(self, obj):
        """Display content preview"""
        if obj.content:
            preview = obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
            from django.utils.html import strip_tags
            return strip_tags(preview)
        return '-'
    get_content_preview.short_description = 'Content Preview'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'submitted_at')
    search_fields = ('name', 'email', 'mobile')
    ordering = ('-submitted_at',)


# ==================== Custom Admin Order Configuration ====================
# Override get_app_list to control model order in admin sidebar
_original_get_app_list = admin.AdminSite.get_app_list

def get_app_list(self, request):
    """
    Custom get_app_list that orders ecommerce models as desired:
    1. Brand, 2. Category, 3. SubCategory, 4. Product, 5. Order
    """
    app_list = _original_get_app_list(self, request)
    
    # Define the desired order for ecommerce app models
    ecommerce_model_order = {
        'Brand': 1,
        'Category': 2,
        'SubCategory': 3,
        'Product': 4,
        'Order': 5,
        'OrderItem': 6,
        'ProductImage': 7,
        'ProductVariation': 8,
        'ProductDetailSection': 9,
        'ContactMessage': 10,
        'CustomUser': 11,
    }
    
    # Reorder models in ecommerce app
    for app in app_list:
        if app['app_label'] == 'ecommerce':
            app['models'].sort(
                key=lambda x: ecommerce_model_order.get(x['object_name'], 999)
            )
    
    return app_list

# Replace the method
admin.AdminSite.get_app_list = get_app_list


class CouponAdminForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    form = CouponAdminForm
    list_display = ('code', 'discount_amount', 'discount_type', 'min_purchase_amount', 'valid_from', 'valid_to', 'active', 'used_count', 'usage_limit', 'created_at')
    list_filter = ('active', 'discount_type', 'valid_from', 'valid_to', 'created_at')
    search_fields = ('code',)
    list_editable = ('active',)
    ordering = ('-created_at',)
    readonly_fields = ('used_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Coupon Information', {
            'fields': ('code', 'discount_amount', 'discount_type')
        }),
        ('Validation Rules', {
            'fields': ('min_purchase_amount', 'valid_from', 'valid_to', 'valid_categories')
        }),
        ('Usage Limits', {
            'fields': ('usage_limit', 'used_count', 'active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('valid_categories')


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'order', 'used_at')
    list_filter = ('used_at', 'coupon')
    search_fields = ('user__email', 'user__mobile', 'coupon__code', 'order__id')
    readonly_fields = ('used_at',)
    ordering = ('-used_at',)
    
    fieldsets = (
        ('Usage Information', {
            'fields': ('user', 'coupon', 'order')
        }),
        ('Timestamps', {
            'fields': ('used_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'coupon', 'order')
