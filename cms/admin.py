from django.contrib import admin
from .models import slider, CMS, profile_setting, Blog, BlogCategory
from django.utils.html import format_html
from django.urls import reverse


@admin.register(slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('ad_title', 'slidercat', 'product', 'deal_type', 'ad_start_date', 'ad_end_date', 'status', 'order', 'post_date', 'author')
    list_filter = ('status', 'deal_type', 'ad_start_date', 'ad_end_date', 'post_date', 'author')
    search_fields = ('ad_title', 'ad_description', 'slidercat__name', 'product__name')
    list_editable = ('status', 'order')
    ordering = ('order', '-post_date')
    list_per_page = 20
    
    fieldsets = (
        ('Slider Information', {
            'fields': ('slidercat', 'sliderimage')
        }),
        ('Slider Ad Details', {
            'fields': ('ad_title', 'ad_description', 'product', 'deal_type', 'ad_start_date', 'ad_end_date')
        }),
        ('Settings', {
            'fields': ('status', 'order', 'author')
        }),
        ('Timestamps', {
            'fields': ('post_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('post_date', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('slug',)
        return self.readonly_fields


@admin.register(CMS)
class CMSAdmin(admin.ModelAdmin):
    list_display = ('pagename', 'status', 'viewcounter', 'order', 'post_date', 'author')
    list_filter = ('status', 'post_date', 'author')
    search_fields = ('pagename', 'Content')
    list_editable = ('status', 'order')
    ordering = ('order', '-post_date')
    list_per_page = 20
    prepopulated_fields = {'slug': ('pagename',)}
    
    fieldsets = (
        ('Page Information', {
            'fields': ('pagename', 'slug', 'Content', 'pageimage')
        }),
        ('SEO Settings', {
            'fields': ('viewcounter', 'post_status'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('status', 'order', 'author')
        }),
        ('Timestamps', {
            'fields': ('post_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('post_date', 'updated_at', 'viewcounter')


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'order', 'created', 'updated')
    list_filter = ('is_active', 'parent', 'created', 'updated')
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'order')
    ordering = ('order', 'name')
    list_per_page = 30
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'description', 'image', 'parent')
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
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('parent')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category', 'get_subcategory', 'author', 'status', 'is_featured', 'order', 'view_counter', 'post_date', 'preview_image')
    list_filter = ('status', 'is_featured', 'category', 'subcategory', 'post_date', 'author')
    search_fields = ('title', 'short_description', 'content')
    list_editable = ('status', 'is_featured', 'order')
    ordering = ('-post_date', 'order')
    list_per_page = 20
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Blog Content', {
            'fields': ('title', 'slug', 'short_description', 'content', 'featured_image')
        }),
        ('Category & Subcategory', {
            'fields': ('category', 'subcategory')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('status', 'is_featured', 'order', 'author')
        }),
        ('Statistics', {
            'fields': ('view_counter',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('post_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('post_date', 'updated_at', 'view_counter')
    
    def get_category(self, obj):
        """Display parent category name"""
        if obj.category:
            return obj.category.name
        return "-"
    get_category.short_description = 'Category'
    get_category.admin_order_field = 'category__name'
    
    def get_subcategory(self, obj):
        """Display subcategory name"""
        if obj.subcategory:
            return obj.subcategory.name
        return "-"
    get_subcategory.short_description = 'Subcategory'
    get_subcategory.admin_order_field = 'subcategory__name'
    
    def preview_image(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 50px;" />',
                obj.featured_image.url
            )
        return "No Image"
    preview_image.short_description = 'Image'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter subcategory choices to only show active subcategories"""
        if db_field.name == "subcategory":
            kwargs["queryset"] = BlogCategory.objects.filter(parent__isnull=False, is_active=True).select_related('parent')
        elif db_field.name == "category":
            kwargs["queryset"] = BlogCategory.objects.filter(parent__isnull=True, is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(profile_setting)
class ProfileSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'email', 'phone_number1', 'create_date')
    list_filter = ('status', 'create_date')
    search_fields = ('email', 'phone_number1', 'phone_number2', 'copyright')
    
    fieldsets = (
        ('Logo Settings', {
            'fields': ('logo_light', 'logo_dark')
        }),
        ('Image Settings', {
            'fields': ('footer_img', 'body_img')
        }),
        ('Theme Colors', {
            'fields': ('background_theme_light', 'background_theme_dark', 'container_background', 'items_background')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone_number1', 'phone_number2')
        }),
        ('Social Media Links', {
            'fields': ('facbook', 'instagram', 'twitter', 'linkedin', 'youtube')
        }),
        ('Address Information', {
            'fields': ('main_office_address', 'branch_office_address', 'google_map')
        }),
        ('Company Information', {
            'fields': ('copyright', 'establish_at')
        }),
        ('Settings', {
            'fields': ('status', 'author')
        }),
        ('Timestamps', {
            'fields': ('create_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('create_date', 'updated_at')
    
    def has_add_permission(self, request):
        # Allow only one profile setting instance
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        if self.model.objects.count() <= 1:
            return False
        return super().has_delete_permission(request, obj)
