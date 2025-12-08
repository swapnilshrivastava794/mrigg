from django.contrib import admin
from .models import Brand, Category, ContactMessage, CustomUser, Product, Order, OrderItem, ProductDetailSection ,ProductImage, ProductVariation
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from django import forms


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image', 'parent', 'is_active', 'order', 'created', 'updated')
    list_filter = ('is_active', 'parent', 'created', 'updated')
    search_fields = ('name',)
    ordering = ('order', 'name')
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug from name
    list_editable = ('is_active', 'order')
    list_per_page = 30
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'image', 'parent')
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


class BrandAdminForm(forms.ModelForm):
    remark = forms.CharField(widget=CKEditorWidget(config_name='description'), required=False)
    
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

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1
    can_delete = True
    fields = ('name', 'quantity', 'unit', 'price_modifier', 'stock')
    verbose_name = 'Variation'
    verbose_name_plural = 'Variations'
    max_num = 20  # Limit number of rows
    
    class Media:
        css = {
            'all': ('admin/css/product_variation_inline.css',)
        }
        js = ('admin/js/product_variation_inline.js',)

class ProductSectionInlineForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name='description'), required=False)
    
    class Meta:
        model = ProductDetailSection
        fields = '__all__'

class ProductSectionInline(admin.TabularInline):
    form = ProductSectionInlineForm
    model = ProductDetailSection
    extra = 1
    can_delete = True
    fields = ('title', 'content')


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(config_name='description'), required=False)
    
    class Meta:
        model = Product
        fields = '__all__'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'get_category', 'get_subcategory', 'brand', 'price','offerprice','popular','latest','featured', 'stock', 'available','short_description', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category', 'category__parent', 'brand']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline , ProductVariationInline , ProductSectionInline]  # ✅ Add this line to show images inline
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Override to filter category choices to only show subcategories"""
        if db_field.name == 'category':
            # Only show categories that have a parent (subcategories)
            # Use a simple filter that doesn't require saved instances
            kwargs['queryset'] = Category.objects.filter(
                parent__isnull=False, 
                is_active=True
            ).select_related('parent').order_by('parent__order', 'parent__name', 'order', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_category(self, obj):
        """Display parent category (main category)"""
        if obj.category and obj.category.parent:
            return obj.category.parent.name
        elif obj.category:
            return obj.category.name
        return '-'
    get_category.short_description = 'Category'
    get_category.admin_order_field = 'category__parent__name'
    
    def get_subcategory(self, obj):
        """Display subcategory"""
        if obj.category and obj.category.parent:
            return obj.category.name
        return '-'
    get_subcategory.short_description = 'Subcategory'
    get_subcategory.admin_order_field = 'category__name'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


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
