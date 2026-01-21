from django.contrib import admin
from .models import slider, CMS, profile_setting, Blog, BlogCategory
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminFileWidget


class SliderForm(forms.ModelForm):
    """Custom form for slider to validate video uploads"""
    class Meta:
        model = slider
        fields = '__all__'
    
    def clean_slidervideo(self):
        """Validate video file type and size"""
        video = self.cleaned_data.get('slidervideo')
        if video:
            # Check file extension
            allowed_extensions = ['.mp4', '.webm', '.ogg', '.mov', '.avi']
            file_extension = video.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise ValidationError(
                    f'Invalid video file type. Allowed types: {", ".join(allowed_extensions)}'
                )
            
            # Check file size (max 50MB)
            if video.size > 50 * 1024 * 1024:
                raise ValidationError('Video file size must be less than 50MB.')
        
        return video
    
    def clean(self):
        """Ensure either image or video is provided, but not both"""
        cleaned_data = super().clean()
        sliderimage = cleaned_data.get('sliderimage')
        slidervideo = cleaned_data.get('slidervideo')
        video_url = cleaned_data.get('video_url')
        
        # Check if fields were explicitly cleared (False means cleared via checkbox)
        image_cleared = sliderimage is False
        video_cleared = slidervideo is False
        
        # If updating existing instance
        if self.instance and self.instance.pk:
            # If image is being cleared, validate that other media exists
            if image_cleared:
                # Don't modify cleaned_data yet - let Django handle False
                # Just validate that other media will be available after clearing
                will_have_video = (slidervideo and slidervideo is not False) or bool(self.instance.slidervideo)
                will_have_video_url = (video_url and video_url.strip() if isinstance(video_url, str) else video_url) or bool(self.instance.video_url)
                
                if not will_have_video and not will_have_video_url:
                    raise ValidationError("Cannot clear image. Please add a video file or video URL first, or keep the existing image.")
            
            # If video is being cleared, validate that other media exists
            if video_cleared:
                # Don't modify cleaned_data yet - let Django handle False
                # Just validate that other media will be available after clearing
                will_have_image = (sliderimage and sliderimage is not False) or bool(self.instance.sliderimage)
                will_have_video_url = (video_url and video_url.strip() if isinstance(video_url, str) else video_url) or bool(self.instance.video_url)
                
                if not will_have_image and not will_have_video_url:
                    raise ValidationError("Cannot clear video. Please add an image or video URL first, or keep the existing video.")
            
            # Preserve existing values if fields weren't changed (not cleared and not new upload)
            if not image_cleared and not sliderimage and self.instance.sliderimage:
                cleaned_data['sliderimage'] = self.instance.sliderimage
                sliderimage = self.instance.sliderimage
            
            if not video_cleared and not slidervideo and self.instance.slidervideo:
                cleaned_data['slidervideo'] = self.instance.slidervideo
                slidervideo = self.instance.slidervideo
            
            if not video_url and self.instance.video_url:
                cleaned_data['video_url'] = self.instance.video_url
                video_url = self.instance.video_url
        
        # Check what media types will be available after processing
        # For cleared fields (False), they will be cleared, so don't count them
        has_image = bool(sliderimage) and sliderimage is not False
        has_video = bool(slidervideo) and slidervideo is not False
        has_video_url = bool(video_url) and (video_url.strip() if isinstance(video_url, str) else True)
        
        # Final validation: At least one media type must be present
        if not has_image and not has_video and not has_video_url:
            if self.instance and self.instance.pk:
                # For updates, if no media in form, check if instance has media (fields weren't changed)
                if not (self.instance.sliderimage or self.instance.slidervideo or self.instance.video_url):
                    raise ValidationError("Please provide either an image, video file, or video URL.")
            else:
                # New instance - must have at least one media
                raise ValidationError("Please provide either an image, video file, or video URL.")
        
        # Validation: Cannot have both image and video
        if has_image and (has_video or has_video_url):
            raise ValidationError("Please provide either an image OR a video (not both).")
        
        # Validation: Cannot have both video file and video URL
        if has_video and has_video_url:
            raise ValidationError("Please provide either a video file OR a video URL (not both).")
        
        return cleaned_data


@admin.register(slider)
class SliderAdmin(admin.ModelAdmin):
    form = SliderForm
    list_display = ('ad_title', 'slidercat', 'product', 'deal_type', 'ad_start_date', 'ad_end_date', 'status', 'order', 'post_date', 'author')
    list_filter = ('status', 'deal_type', 'ad_start_date', 'ad_end_date', 'post_date', 'author')
    search_fields = ('ad_title', 'ad_description', 'slidercat__name', 'product__name')
    list_editable = ('status', 'order')
    ordering = ('order', '-post_date')
    list_per_page = 20
    
    fieldsets = (
        ('Slider Media (Choose ONE option)', {
            'fields': ('sliderimage', 'slidervideo', 'video_url'),
            'description': 'Upload an IMAGE OR a VIDEO FILE OR provide a VIDEO URL (YouTube/Vimeo). Do not use multiple options.'
        }),
        ('Slider Information', {
            'fields': ('slidercat',)
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
    
    def get_queryset(self, request):
        """Optimize queryset to avoid N+1 queries"""
        qs = super().get_queryset(request)
        return qs.select_related('slidercat', 'product', 'author')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('slug',)
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        """Override save to optimize performance and handle cleared fields"""
        # Set author if not set
        if not obj.author_id:
            obj.author = request.user
        
        # Handle cleared file fields - convert False to None for database
        if obj.sliderimage is False:
            obj.sliderimage = None
        if obj.slidervideo is False:
            obj.slidervideo = None
        
        # Check if image field was actually changed using form's changed_data
        if change and 'sliderimage' not in form.changed_data:
            # Image wasn't changed, skip image processing for faster save
            obj.save(skip_image_processing=True)
        else:
            # Image was changed or new object, use normal save
            super().save_model(request, obj, form, change)


class CMSFileWidget(AdminFileWidget):
    """Custom widget that allows both clear checkbox and file upload"""
    def value_from_datadict(self, data, files, name):
        """Override to handle both clear checkbox and file upload"""
        upload = files.get(name)
        clear = data.get(f"{name}-clear", False)
        
        # If both are provided, prioritize the new file (ignore clear checkbox)
        if upload and clear:
            return upload
        
        # If only clear checkbox is checked
        if clear:
            return False
        
        # If only file is uploaded
        if upload:
            return upload
        
        # If neither, return None (will keep existing file)
        return None


class CMSForm(forms.ModelForm):
    """Custom form for CMS to handle image uploads properly"""
    class Meta:
        model = CMS
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make pageimage optional for updates
        if self.instance and self.instance.pk:
            self.fields['pageimage'].required = False
            # Use custom widget
            self.fields['pageimage'].widget = CMSFileWidget()
    
    def clean_pageimage(self):
        """Handle image field validation"""
        pageimage = self.cleaned_data.get('pageimage')
        
        # If pageimage is False, it means clear checkbox was checked
        # Django will handle this automatically, we just need to allow it
        if pageimage is False:
            return False
        
        # If a new file is uploaded, validate it
        if pageimage:
            # Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            file_extension = pageimage.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise ValidationError(
                    f'Invalid image file type. Allowed types: {", ".join(allowed_extensions)}'
                )
        
        return pageimage


@admin.register(CMS)
class CMSAdmin(admin.ModelAdmin):
    form = CMSForm
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
    
    def get_queryset(self, request):
        """Optimize queryset to avoid N+1 queries"""
        qs = super().get_queryset(request)
        return qs.select_related('author')
    
    def save_model(self, request, obj, form, change):
        """Override save to handle cleared image fields properly"""
        # Set author if not set
        if not obj.author_id:
            obj.author = request.user
        
        # Handle cleared image field - convert False to None for database
        if obj.pageimage is False:
            obj.pageimage = None
        
        # Save the model
        super().save_model(request, obj, form, change)


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
    search_fields = ('title', 'short_description', 'content', 'tags')
    list_editable = ('status', 'is_featured', 'order')
    ordering = ('-post_date', 'order')
    list_per_page = 20
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Blog Content', {
            'fields': ('title', 'slug', 'short_description', 'content', 'featured_image', 'tags')
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
    
    def get_queryset(self, request):
        """Optimize queryset to avoid N+1 queries"""
        qs = super().get_queryset(request)
        return qs.select_related('category', 'subcategory', 'author')
    
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


class ProfileSettingForm(forms.ModelForm):
    """Custom form to validate logo file types"""
    class Meta:
        model = profile_setting
        fields = '__all__'
    
    def clean_logo_light(self):
        logo_light = self.cleaned_data.get('logo_light')
        if logo_light:
            allowed_extensions = ['.svg', '.png', '.jpg', '.jpeg', '.webp']
            file_extension = logo_light.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise ValidationError(
                    f'Invalid file type. Allowed types: {", ".join(allowed_extensions)}'
                )
        return logo_light
    
    def clean_logo_dark(self):
        logo_dark = self.cleaned_data.get('logo_dark')
        if logo_dark:
            allowed_extensions = ['.svg', '.png', '.jpg', '.jpeg', '.webp']
            file_extension = logo_dark.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise ValidationError(
                    f'Invalid file type. Allowed types: {", ".join(allowed_extensions)}'
                )
        return logo_dark


@admin.register(profile_setting)
class ProfileSettingAdmin(admin.ModelAdmin):
    form = ProfileSettingForm
    list_display = ('id', 'status', 'email', 'phone_number1', 'create_date')
    list_filter = ('status', 'create_date')
    search_fields = ('email', 'phone_number1', 'phone_number2', 'copyright')
    
    fieldsets = (
        ('Logo Settings', {
            'fields': ('logo_light', 'logo_dark'),
            'description': 'Upload SVG, PNG, JPG, or WebP files for logos. SVG files are recommended for scalability.'
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
