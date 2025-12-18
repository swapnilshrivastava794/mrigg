from django.contrib import admin
from .models import Brand, Category, SubCategory, ContactMessage, CustomUser, Product, Order, OrderItem, ProductDetailSection ,ProductImage, ProductVariation
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from django import forms
import logging
import time
from django.db import connection, reset_queries

# Setup logger
logger = logging.getLogger('ecommerce.admin')


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


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    can_delete = True
    max_num = 10  # Limit number of images
    show_change_link = False  # Disable change link for faster loading
    
    def get_queryset(self, request):
        """Optimize queryset for inline"""
        qs = super().get_queryset(request)
        return qs.only('id', 'image', 'alt_text', 'product_id')

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

class ProductSectionInline(admin.TabularInline):
    form = ProductSectionInlineForm
    model = ProductDetailSection
    extra = 1
    can_delete = True
    fields = ('title', 'content')
    max_num = 10  # Limit number of sections
    show_change_link = False  # Disable change link for faster loading
    
    def get_queryset(self, request):
        """Optimize queryset for inline"""
        qs = super().get_queryset(request)
        return qs.only('id', 'title', 'content', 'product_id')


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

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'get_category', 'get_subcategory', 'price','offerprice','popular','latest','featured', 'stock', 'available', 'created', 'updated']
    # Simplified list_filter - use subcategory and brand
    list_filter = ['available', 'created', 'updated', 'subcategory', 'subcategory__category', 'brand']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 50  # Limit items per page to reduce load
    show_full_result_count = False  # Disable full count for faster loading
    inlines = [ProductImageInline , ProductVariationInline , ProductSectionInline]  # ✅ Add this line to show images inline
    
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

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    
    def get_queryset(self, request):
        """Optimize queryset for inline"""
        qs = super().get_queryset(request)
        return qs.select_related('product')

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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'submitted_at')
    search_fields = ('name', 'email', 'mobile')
    ordering = ('-submitted_at',)
