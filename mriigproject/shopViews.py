from django.shortcuts import render, get_object_or_404
from ecommerce.models import Category, SubCategory, Product

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
      if not category_slug:
          category_slug = request.GET.get('category', None)
      if not subcategory_slug:
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
       'title':'Shop',
       'subTitle':'Shop',
       'subTitle2':'Shop',
       'css':'<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
       'css2':'<link rel="stylesheet" type="text/css" href="/static/css/jquery.nstSlider.min.css"/>',
       'footer':'true',
       'script':'<script src="/static/js/vendors/zoom.js"></script>  <script src="/static/js/vendors/jquery.nstSlider.min.js"></script>',
       'categories': categories,
       'products': products,
       'selected_category': selected_category,
       'selected_subcategory': selected_subcategory,
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