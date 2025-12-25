from django.shortcuts import render, get_object_or_404
from ecommerce.models import Category, SubCategory, Product, Brand

def account(request):     
      data = {
       'title':'Account',
       'subTitle':'Shop',
       'subTitle2':'Account',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
       'footer':'true',
       'script':'<script src="/static/js/vendors/zoom.js"></script>',
      }
      return render(request, "shop/account.html", data)

def cart(request):     
      data = {
       'title':'Cart',
       'subTitle':'Shop',
       'subTitle2':'Cart',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
       'footer':'true',
       'script':'<script src="/static/js/vendors/zoom.js"></script>',
      }
      return render(request, "shop/cart.html", data)

def checkOut(request):     
      data = {
       'title':'Checkout',
       'subTitle':'Shop',
       'subTitle2':'Checkout',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
       'footer':'true',
       'script':'<script src="/static/js/vendors/zoom.js"></script>',
      }
      return render(request, "shop/checkOut.html", data)

def fullWidthShop(request):     
      data = {
       'title':'Full Width Shop',
       'subTitle':'Shop',
       'subTitle2':'Full Width Shop',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/> <link rel="stylesheet" type="text/css" href="/static/css/jquery.nstSlider.min.css"/>',
       'script':'<script src="/static/js/vendors/zoom.js"></script>  <script src="/static/js/vendors/jquery.nstSlider.min.js"></script>',
       'footer':'true',
      }
      return render(request, "shop/fullWidthShop.html", data)

def groupedProducts(request):     
      data = {
       'title':'Grouped Product',
       'subTitle':'Shop',
       'subTitle2':'Grouped Product',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
       'footer':'true',
      }
      return render(request, "shop/groupedProducts.html", data)

def productDetails(request):     
      data = {
       'title':'Product',
       'subTitle':'Shop',
       'subTitle2':'Product',
       'footer':'true',
       'script':'<script src="/static/js/vendors/zoom.js"></script>',
      }
      return render(request, "shop/productDetails.html", data)

def productDetails2(request):     
      data = {
       'title':'Product',
       'subTitle':'Shop',
       'subTitle2':'Product',
       'footer':'true',
       'script':'<script src="/static/js/vendors/zoom.js"></script> ',
      }
      return render(request, "shop/productDetails2.html", data)

def shop(request, category_slug=None, subcategory_slug=None):
      # Get filter parameters from URL or query string (for backward compatibility)
      # Note: category_slug and subcategory_slug come from URL path, filters come from query string
      
      # Get all categories for sidebar
      categories = Category.objects.filter(is_active=True).prefetch_related('subcategories').order_by('order')
      
      # Add active subcategories to each category for template
      for category in categories:
          category.active_subcategory_count = category.subcategories.filter(is_active=True).count()
          category.active_subcategories = list(category.subcategories.filter(is_active=True))
      
      # Get all products first
      products = Product.objects.filter(is_active=True).select_related('subcategory', 'subcategory__category', 'brand').prefetch_related('images', 'variations').order_by('-id')
      
      # Filter by category if provided
      if subcategory_slug:
          subcategory = get_object_or_404(SubCategory, slug=subcategory_slug, is_active=True)
          products = products.filter(subcategory=subcategory)
          selected_category = subcategory.category
          selected_subcategory = subcategory
      elif category_slug:
          category = get_object_or_404(Category, slug=category_slug, is_active=True)
          # Get all subcategories of this category
          subcategories = SubCategory.objects.filter(category=category, is_active=True)
          # Get products from all subcategories
          products = products.filter(subcategory__in=subcategories)
          selected_category = category
          selected_subcategory = None
      else:
          selected_category = None
          selected_subcategory = None
      
      # Get all active brands from database
      # Show brands that have products in the current category/subcategory, or all active brands
      base_products = products  # Products filtered by category/subcategory
      brand_ids_in_category = list(base_products.exclude(brand__isnull=True).values_list('brand_id', flat=True).distinct())
      
      if brand_ids_in_category:
          # Show only brands that have products in current category/subcategory
          brands = Brand.objects.filter(id__in=brand_ids_in_category, is_active=True).order_by('order', 'name')
      else:
          # If no brands in current category, show all active brands that have any products
          all_brand_ids = Product.objects.filter(
              is_active=True, 
              brand__isnull=False,
              brand__is_active=True
          ).values_list('brand_id', flat=True).distinct()
          
          if all_brand_ids:
              brands = Brand.objects.filter(id__in=all_brand_ids, is_active=True).order_by('order', 'name')
          else:
              # Last fallback: show all active brands
              brands = Brand.objects.filter(is_active=True).order_by('order', 'name')
      
      # Apply filters from query parameters
      # Price filter - get effective price (offerprice if > 0, else price)
      price_min = request.GET.get('price_min')
      price_max = request.GET.get('price_max')
      if price_min:
          try:
              price_min = float(price_min)
              from django.db.models import Q, Case, When, F, DecimalField
              # Filter products where effective price >= price_min
              products = products.annotate(
                  effective_price=Case(
                      When(offerprice__gt=0, then=F('offerprice')),
                      default=F('price'),
                      output_field=DecimalField()
                  )
              ).filter(effective_price__gte=price_min)
          except (ValueError, TypeError):
              pass
      if price_max:
          try:
              price_max = float(price_max)
              from django.db.models import Q, Case, When, F, DecimalField
              # Ensure effective_price annotation exists
              if 'effective_price' not in [f.name for f in products.model._meta.get_fields()]:
                  products = products.annotate(
                      effective_price=Case(
                          When(offerprice__gt=0, then=F('offerprice')),
                          default=F('price'),
                          output_field=DecimalField()
                      )
                  )
              products = products.filter(effective_price__lte=price_max)
          except (ValueError, TypeError):
              pass
      
      # Brand filter
      brand_slug = request.GET.get('brand')
      if brand_slug:
          products = products.filter(brand__slug=brand_slug, brand__is_active=True)
      
      # Color filter
      color = request.GET.get('color')
      if color:
          # Filter products that have this color in variations or product color_code
          from django.db.models import Q
          products = products.filter(
              Q(variations__color_code=color) | Q(color_code=color)
          ).distinct()
      
      # Get unique colors from products and variations
      from django.db.models import Q
      color_codes = set()
      # Get colors from product variations
      from ecommerce.models import ProductVariation
      variation_colors = ProductVariation.objects.filter(
          product__in=products, color_code__isnull=False
      ).exclude(color_code='').values_list('color_code', flat=True).distinct()
      color_codes.update(variation_colors)
      # Get colors from products
      product_colors = products.exclude(color_code__isnull=True).exclude(color_code='').values_list('color_code', flat=True).distinct()
      color_codes.update(product_colors)
      
      # Get min and max prices for price filter range
      from django.db.models import Min, Max, Q, Case, When, F, DecimalField
      price_stats = products.aggregate(
          min_price=Min(
              Case(
                  When(offerprice__gt=0, then=F('offerprice')),
                  default=F('price'),
                  output_field=DecimalField()
              )
          ),
          max_price=Max(
              Case(
                  When(offerprice__gt=0, then=F('offerprice')),
                  default=F('price'),
                  output_field=DecimalField()
              )
          )
      )
      
      # Get product count
      product_count = products.count()
      
      data = {
       'title':'Shop',
       'subTitle':'Shop',
       'subTitle2':'Shop',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
       'css2':'<link rel="stylesheet" type="text/css" href="/static/css/jquery.nstSlider.min.css"/>',
       'footer':'true',
       'script':'<script src="/static/js/vendors/zoom.js"></script>  <script src="/static/js/vendors/jquery.nstSlider.min.js"></script>',
       'categories': categories,
       'products': products,
       'brands': brands,
       'selected_category': selected_category,
       'selected_subcategory': selected_subcategory,
       'product_count': product_count,
       'colors': sorted(list(color_codes)),
       'price_min': price_stats.get('min_price', 0) or 0,
       'price_max': price_stats.get('max_price', 10000) or 10000,
       'current_price_min': price_min if price_min else (price_stats.get('min_price', 0) or 0),
       'current_price_max': price_max if price_max else (price_stats.get('max_price', 10000) or 10000),
       'selected_brand': brand_slug,
       'selected_color': color,
      }
      return render(request, "shop/shop.html", data)

def sidebarLeft(request):
      # Get filter parameters
      category_slug = request.GET.get('category', None)
      subcategory_slug = request.GET.get('subcategory', None)
      
      # Get all categories for sidebar
      categories = Category.objects.filter(is_active=True).prefetch_related('subcategories').order_by('order')
      
      # Get all products
      products = Product.objects.filter(is_active=True).select_related('subcategory', 'subcategory__category', 'brand').prefetch_related('images').order_by('-id')
      
      # Filter by category if provided
      if subcategory_slug:
          subcategory = get_object_or_404(SubCategory, slug=subcategory_slug, is_active=True)
          products = products.filter(subcategory=subcategory)
          selected_category = subcategory.category
          selected_subcategory = subcategory
      elif category_slug:
          category = get_object_or_404(Category, slug=category_slug, is_active=True)
          # Get all subcategories of this category
          subcategories = SubCategory.objects.filter(category=category, is_active=True)
          # Get products from all subcategories
          products = products.filter(subcategory__in=subcategories)
          selected_category = category
          selected_subcategory = None
      else:
          selected_category = None
          selected_subcategory = None
      
      data = {
       'title':'Slidebar Left',
       'subTitle':'Shop',
       'subTitle2':'Slidebar Left',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/> <link rel="stylesheet" type="text/css" href="/static/css/jquery.nstSlider.min.css"/>',
       'script':'<script src="/static/js/vendors/zoom.js"></script>  <script src="/static/js/vendors/jquery.nstSlider.min.js"></script>',
       'footer':'true',
       'categories': categories,
       'products': products,
       'selected_category': selected_category,
       'selected_subcategory': selected_subcategory,
      }
      return render(request, "shop/sidebarLeft.html", data)

def sidebarRight(request):     
      data = {
       'title':'Slidebar Right',
       'subTitle':'Shop',
       'subTitle2':'Slidebar Right',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/> <link rel="stylesheet" type="text/css" href="/static/css/jquery.nstSlider.min.css"/>',
       'script':'<script src="/static/js/vendors/zoom.js"></script>  <script src="/static/js/vendors/jquery.nstSlider.min.js"></script>',
      }
      return render(request, "shop/sidebarRight.html", data)

def variableProducts(request):     
      data = {
       'title':'Variable Product',
       'subTitle':'Shop',
       'subTitle2':'Variable Product',
       'script':'<script src="/static/js/vendors/jquery.nstSlider.min.js"></script> <script src="/static/js/vendors/zoom.js"></script>',
       'footer':'true',
      }
      return render(request, "shop/variableProducts.html", data)