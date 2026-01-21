from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from io import BytesIO

# Try to import optional fields, use standard Django fields if not available
try:
    from image_cropping import ImageCropField, ImageRatioField
except ImportError:
    ImageCropField = models.ImageField
    ImageRatioField = None

try:
    from autoslug import AutoSlugField
except ImportError:
    from django.db import models
    AutoSlugField = models.SlugField

try:
    from ckeditor_uploader.fields import RichTextUploadingField
except ImportError:
    from django.db import models
    RichTextUploadingField = models.TextField

# Create your models here.

     
class slider(models.Model):
    # Using Category from ecommerce app - adjust if you have a different category model
    id = models.BigAutoField(primary_key=True)
    slidercat=models.ForeignKey("ecommerce.Category", verbose_name="Select Category",null=True,blank=True,on_delete=models.CASCADE)
    sliderimage = models.ImageField(upload_to='slider/', null=True, blank=True, verbose_name="Slider Image (1400X520px)", help_text="Upload an image OR a video (not both)")
    slidervideo = models.FileField(upload_to='slider/videos/', null=True, blank=True, verbose_name="Slider Video", help_text="Upload a video file (mp4, webm, ogg) OR use image above")
    video_url = models.URLField(max_length=500, null=True, blank=True, verbose_name="Video URL (YouTube/Vimeo)", help_text="Optional: YouTube or Vimeo video URL")
    
    # New fields for slider ad
    ad_title = models.CharField(max_length=200, verbose_name="Ad Title", null=True, blank=True, help_text="Title for the slider advertisement")
    ad_description = models.TextField(verbose_name="Ad Description", null=True, blank=True, help_text="Description for the slider advertisement")
    product = models.ForeignKey("ecommerce.Product", verbose_name="Product", null=True, blank=True, on_delete=models.SET_NULL, help_text="Select a product to link to this slider ad (160 character only)")
    DEAL_TYPE_CHOICES = (
        ('hot_deals', 'Hot Deal(Main slider)'),
        ('best_summer_deal', 'Best Summer Deal'),
        ('best_sale_product', 'Best Sale Product'),
        ('high_demand_product', 'High Demand Product'),
        ('others', 'Others'),
    )
    deal_type = models.CharField(max_length=50, choices=DEAL_TYPE_CHOICES, null=True, blank=True, verbose_name="Deal Type", help_text="Select the type of deal for this slider ad")
    ad_start_date = models.DateField(verbose_name="Ad Start Date", null=True, blank=True, help_text="Start date for when this ad should be displayed")
    ad_end_date = models.DateField(verbose_name="Ad End Date", null=True, blank=True, help_text="End date for when this ad should stop being displayed")
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure either image or video is provided, but not both
        has_image = bool(self.sliderimage)
        has_video = bool(self.slidervideo)
        has_video_url = bool(self.video_url)
        
        if not has_image and not has_video and not has_video_url:
            raise ValidationError("Please provide either an image, video file, or video URL.")
        
        if has_image and (has_video or has_video_url):
            raise ValidationError("Please provide either an image OR a video (not both).")
        
        if has_video and has_video_url:
            raise ValidationError("Please provide either a video file OR a video URL (not both).")
    
    def save(self, *args, **kwargs):
        # Skip image processing if requested (for faster updates)
        skip_image_processing = kwargs.pop('skip_image_processing', False)
        
        # Auto-generate slug from ad_title if not provided
        if not self.slug and self.ad_title:
            from django.utils.text import slugify
            self.slug = slugify(self.ad_title)
            # Ensure uniqueness - optimize by checking only if slug exists
            if slider.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                base_slug = self.slug
                counter = 1
                while slider.objects.filter(slug=f"{base_slug}-{counter}").exclude(pk=self.pk).exists():
                    counter += 1
                self.slug = f"{base_slug}-{counter}"
        
        # Save first to get the file path
        super(slider, self).save(*args, **kwargs)
        
        # Resize the image ONLY if not skipped and image exists
        if not skip_image_processing and self.sliderimage:
            try:
                # Check if file exists and is an image
                if hasattr(self.sliderimage, 'path') and self.sliderimage.path:
                    # Check if file actually exists on disk
                    import os
                    if os.path.exists(self.sliderimage.path):
                        # Check if file was just uploaded (has _upload suffix or is new)
                        img = Image.open(self.sliderimage.path)
                        # Check current size - only resize if larger than target
                        if img.size[0] > 1400 or img.size[1] > 520:
                            # Resize to max 1400x520 while maintaining aspect ratio
                            img.thumbnail((1400, 520), Image.Resampling.LANCZOS)
                            img.save(self.sliderimage.path, optimize=True, quality=85)
            except Exception:
                # If it's not an image or processing fails, skip
                pass
    
    slug=models.SlugField(max_length=200, unique=True, null=True, blank=True, verbose_name="Slug")
    post_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order=models.IntegerField(unique=False,null=True,default=5,verbose_name="Order")
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    # author = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
    author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)
    def is_video(self):
        """Check if slider has video (file or URL)"""
        return bool(self.slidervideo or self.video_url)
    
    def is_image(self):
        """Check if slider has image"""
        return bool(self.sliderimage)
    
    def get_media_type(self):
        """Return 'video' or 'image' based on what's available"""
        if self.is_video():
            return 'video'
        elif self.is_image():
            return 'image'
        return None
    
    def get_video_mime_type(self):
        """Get correct MIME type for video file based on extension"""
        if not self.slidervideo:
            return 'video/mp4'  # Default
        
        video_name = str(self.slidervideo.name).lower()
        
        if video_name.endswith('.mp4'):
            return 'video/mp4'
        elif video_name.endswith('.webm'):
            return 'video/webm'
        elif video_name.endswith('.ogg') or video_name.endswith('.ogv'):
            return 'video/ogg'
        elif video_name.endswith('.mov'):
            return 'video/quicktime'
        elif video_name.endswith('.avi'):
            return 'video/x-msvideo'
        else:
            return 'video/mp4'  # Default fallback
    
    def delete(self, *args, **kwargs):
        """Override delete to also delete associated files from storage"""
        # Store file names and storage references before deletion
        image_name = None
        video_name = None
        image_storage = None
        video_storage = None
        
        # Get image file name and storage if exists
        if self.sliderimage:
            image_name = self.sliderimage.name
            image_storage = self.sliderimage.storage
        
        # Get video file name and storage if exists
        if self.slidervideo:
            video_name = self.slidervideo.name
            video_storage = self.slidervideo.storage
        
        # Delete the model instance first
        super(slider, self).delete(*args, **kwargs)
        
        # Delete image file from storage
        if image_name and image_storage:
            try:
                # Use storage.delete() which works with all storage backends
                image_storage.delete(image_name)
            except Exception:
                # Fallback: try direct file deletion if storage.delete fails
                try:
                    import os
                    from django.conf import settings
                    image_path = os.path.join(settings.MEDIA_ROOT, image_name)
                    if os.path.exists(image_path):
                        os.remove(image_path)
                except Exception:
                    pass
        
        # Delete video file from storage
        if video_name and video_storage:
            try:
                # Use storage.delete() which works with all storage backends
                video_storage.delete(video_name)
            except Exception:
                # Fallback: try direct file deletion if storage.delete fails
                try:
                    import os
                    from django.conf import settings
                    video_path = os.path.join(settings.MEDIA_ROOT, video_name)
                    if os.path.exists(video_path):
                        os.remove(video_path)
                except Exception:
                    pass
    
    def get_video_embed_url(self):
        """Get embed URL for YouTube/Vimeo videos"""
        if not self.video_url:
            return None
        
        import re
        
        # YouTube URL patterns
        youtube_patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in youtube_patterns:
            match = re.search(pattern, self.video_url)
            if match:
                video_id = match.group(1)
                return f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0&showinfo=0&rel=0"
        
        # Vimeo URL pattern
        vimeo_pattern = r'vimeo\.com\/(?:.*\/)?(\d+)'
        match = re.search(vimeo_pattern, self.video_url)
        if match:
            video_id = match.group(1)
            return f"https://player.vimeo.com/video/{video_id}?autoplay=1&muted=1&loop=1&controls=0"
        
        return None
    
    def is_youtube_or_vimeo(self):
        """Check if video URL is YouTube or Vimeo"""
        if not self.video_url:
            return False
        return 'youtube.com' in self.video_url or 'youtu.be' in self.video_url or 'vimeo.com' in self.video_url
    
    def __str__(self):
        return self.ad_title or f"Slider {self.id}"
    
    class Meta:
        ordering = ['order']
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"

class CMS(models.Model):
    id = models.BigAutoField(primary_key=True)
    pagename=models.CharField(max_length=150, verbose_name="Page Name",null=True,default=None)
    Content=RichTextUploadingField(null=True,default='No News', verbose_name="Long Discretion")
    pageimage = models.ImageField(upload_to='cms/', null=True, blank=True, verbose_name="Page Image (1280X220px)")
    
    def save(self, *args, **kwargs):
        super(CMS, self).save(*args, **kwargs)
        if self.pageimage:
            # Check if file actually exists before processing
            import os
            if os.path.exists(self.pageimage.path):
                try:
                    img = Image.open(self.pageimage.path)
                    desired_size = (1280, 220)
                    img.thumbnail(desired_size)
                    img.save(self.pageimage.path)
                except Exception as e:
                    # If image processing fails, log but don't break save
                    print(f"Error processing CMS image: {e}")
    
    slug=models.SlugField(max_length=200, unique=True, null=True, blank=True, verbose_name="Slug")
    post_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    viewcounter = models.IntegerField(unique=False,null=True,default=0,verbose_name="Views")
    post_status=models.IntegerField(verbose_name="Counter",null=True,default=100)
    order=models.IntegerField(unique=False,null=True,default=5,verbose_name="Order")
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    # author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='setting_cms_entries') 
    author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)
    def __str__(self):
        return self.pagename
    
    def get_absolute_url(self):
         return reverse('cms', args=[self.slug])
    
    class Meta:
        ordering = ['order']
        verbose_name = "Content Management System"  


class profile_setting(models.Model):
    id = models.BigAutoField(primary_key=True)
    logo_light = models.FileField(upload_to='logo/', null=True, blank=True, verbose_name="Logo Light (SVG, PNG, JPG - 500X100px)", help_text="Accepts SVG, PNG, JPG files")
    logo_dark = models.FileField(upload_to='logo/', null=True, blank=True, verbose_name="Logo Dark (SVG, PNG, JPG - 500X100px)", help_text="Accepts SVG, PNG, JPG files")
    footer_img = models.ImageField(upload_to='profile_image/', null=True, blank=True, verbose_name="Footer Image (1920X365px)")
    body_img =  models.ImageField(upload_to='profile_image/', null=True, blank=True, verbose_name="Body Image (1920X365px)")
    background_theme_light = models.CharField(max_length=7, null=True, blank=True, default="#FFFFFF", verbose_name="background Theme Light", help_text="Light Background")
    background_theme_dark = models.CharField(max_length=7, null=True, blank=True, default="#000000", verbose_name="background Theme Dark", help_text="Dark Background")
    container_background = models.CharField(max_length=7, null=True, blank=True, default="#fcf8e7", verbose_name="container background", help_text="container background in body")
    items_background = models.CharField(max_length=7, null=True, blank=True, default="#FFFFFF", verbose_name="Items background", help_text="items background in body")
    email = models.EmailField(max_length=150, null=True, blank=True)
    phone_number1 = models.CharField(max_length=20, null=True, blank=True, verbose_name="Phone Number 1")
    phone_number2 = models.CharField(max_length=20, null=True, blank=True, verbose_name="Phone Number 2")
    facbook = models.URLField(null=True, blank=True, verbose_name="Facebook")
    instagram = models.URLField(null=True, blank=True, verbose_name="Instagram")
    twitter = models.URLField(null=True, blank=True, verbose_name="Twitter")
    linkedin = models.URLField(null=True, blank=True, verbose_name="Linkedin")
    youtube = models.URLField(null=True, blank=True, verbose_name="Youtube")
    main_office_address = models.TextField(max_length=200, null=True, blank=True, verbose_name="Main Office Address")
    branch_office_address = models.TextField(max_length=255, null=True, blank=True, verbose_name="Branch Office Address")
    google_map = models.TextField(null=True, blank=True, verbose_name="Google Map", help_text="Embed Code")
    copyright = models.CharField(max_length=255, null=True, blank=True, verbose_name="Copyright")
    establish_at = models.DateField(null=True, blank=True, verbose_name="Establish At")
    create_date=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    # author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='setting_entries') 
    author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)
    class Meta:
        verbose_name = "Profile Setting"
    
    def __str__(self):
        return str(self.id)


class BlogCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Category Name")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='blog/categories/', null=True, blank=True, verbose_name="Category Image (250X250px)")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        blank=True,
        null=True,
        verbose_name="Parent Category"
    )
    is_active = models.BooleanField(default=True, verbose_name="Status")
    order = models.IntegerField(null=True, default=None, verbose_name="Order", blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug and self.name:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
            # Ensure uniqueness
            base_slug = self.slug
            counter = 1
            while BlogCategory.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        
        super(BlogCategory, self).save(*args, **kwargs)
        
        # Process image if provided
        if self.image:
            try:
                img = Image.open(self.image.path)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
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
                img.save(self.image.path)
            except Exception:
                pass

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} / {self.name}"
        return self.name


class Blog(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Blog Title")
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True, verbose_name="Slug")
    short_description = models.CharField(max_length=300, null=True, blank=True, verbose_name="Short Description")
    content = RichTextUploadingField(null=True, blank=True, verbose_name="Content")
    featured_image = models.ImageField(upload_to='blog/', null=True, blank=True, verbose_name="Featured Image (800X400px)")
    category = models.ForeignKey(
        'BlogCategory',
        related_name='blogs',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Blog Category",
        help_text="Select main category (parent category)"
    )
    subcategory = models.ForeignKey(
        'BlogCategory',
        related_name='subcategory_blogs',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Blog Subcategory",
        help_text="Select subcategory (child category)",
        limit_choices_to={'parent__isnull': False}
    )
    # author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='blog_entries')
    author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
)
    post_date = models.DateTimeField(auto_now_add=True, verbose_name="Published Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    view_counter = models.IntegerField(default=0, verbose_name="Views")
    order = models.IntegerField(null=True, default=0, verbose_name="Order")
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Status")
    is_featured = models.BooleanField(default=False, verbose_name="Featured Post")
    tags = models.CharField(max_length=500, null=True, blank=True, verbose_name="Tags", help_text="Comma-separated tags (e.g., Cosmetics, Makeup, Skincare)")
    meta_title = models.CharField(max_length=200, null=True, blank=True, verbose_name="Meta Title (SEO)")
    meta_description = models.TextField(max_length=300, null=True, blank=True, verbose_name="Meta Description (SEO)")
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug and self.title:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
            # Ensure uniqueness
            base_slug = self.slug
            counter = 1
            while Blog.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        
        super(Blog, self).save(*args, **kwargs)
        
        # Resize featured image if provided
        if self.featured_image:
            try:
                img = Image.open(self.featured_image.path)
                # Resize to max 800x400 while maintaining aspect ratio
                img.thumbnail((800, 400), Image.Resampling.LANCZOS)
                img.save(self.featured_image.path)
            except Exception:
                pass
    
    def get_absolute_url(self):
        return reverse('blog-detail', args=[self.slug])
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    class Meta:
        ordering = ['-post_date', 'order']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
    def __str__(self):
        return self.title

