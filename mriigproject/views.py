from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.db.models import Q, Count
from datetime import date

from ecommerce.models import Category, ContactMessage, CustomUser, Order, OrderItem, Product
from cms.models import slider
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from ecommerce.decorators import custom_login_required






# Create your views here.

# def home(request):
#     categories = Category.objects.all()
#     products = Product.objects.prefetch_related('images').all()
#     return render(request, 'main/index.html', {
#         'categories': categories,
#         'products': products
#     })

def home(request):
    # Get all active parent categories with their subcategories
    all_categories = Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('subcategories').order_by('order')
    
    # Get limited categories for other sections (if needed)
    categories = Category.objects.filter(parent__isnull=True, is_active=True).order_by('order')[:6]
    
    # Get categories with images for New Collection section (limit to 4-6 categories)
    # Count products from all subcategories of each parent category
    collection_categories = Category.objects.filter(
        parent__isnull=True, 
        is_active=True,
        image__isnull=False
    ).prefetch_related('subcategories').order_by('order')[:6]
    
    # Calculate product count for each category (including subcategories)
    for cat in collection_categories:
        subcategory_ids = list(cat.subcategories.filter(is_active=True).values_list('id', flat=True))
        if subcategory_ids:
            cat.product_count = Product.objects.filter(
                category_id__in=subcategory_ids,
                is_active=True
            ).count()
        else:
            cat.product_count = 0
    
    #products = Product.objects.filter(is_active=True).order_by('-id')[:12]
    featured = Product.objects.filter(is_active=True, featured=True).prefetch_related('images').order_by('-id')[:12]
    popular = Product.objects.filter(is_active=True, popular=True).prefetch_related('images').order_by('id')[:12]
    latest = Product.objects.filter(is_active=True, latest=True).prefetch_related('images').order_by('-id')[:12]
    
    # Get active sliders with date filtering - Show only Hot Deals
    today = date.today()
    sliders = slider.objects.filter(
        status='active',
        deal_type='hot_deals'  # Show only Hot Deal sliders
    ).filter(
        # Filter by date range if dates are set
        # Show slider if:
        # 1. No start date set OR start date <= today
        # 2. AND (No end date set OR end date >= today)
        Q(ad_start_date__isnull=True) | Q(ad_start_date__lte=today),
        Q(ad_end_date__isnull=True) | Q(ad_end_date__gte=today)
    ).select_related('product', 'slidercat').order_by('order', '-post_date')
    
    return render(request, 'home/index.html', {
        'categories': categories,
        'all_categories': all_categories,  # All categories with subcategories for sidebar
        'collection_categories': collection_categories,  # Categories for New Collection section
        'fl': featured,
        'pl': popular,
        'lts': latest,
        'sliders': sliders,  # Add sliders to context
        'footer': True,  # Show footer
    })
    
def aboutus(request):
    categories = Category.objects.prefetch_related('subcategories').filter(parent__isnull=True)
    products = Product.objects.prefetch_related('images').all()
    return render(request, 'main/about-us.html', {
        'categories': categories,
        'products': products
    })
    
def ourproduct(request):
    # Get filter parameters
    category_slug = request.GET.get('category', None)
    subcategory_slug = request.GET.get('subcategory', None)
    
    # Get all categories for sidebar
    categories = Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('subcategories').order_by('order')
    
    # Get all active products
    products = Product.objects.filter(is_active=True).select_related('category', 'category__parent', 'brand').prefetch_related('images').order_by('-id')
    
    # Filter by category if provided
    if subcategory_slug:
        subcategory = get_object_or_404(Category, slug=subcategory_slug, is_active=True, parent__isnull=False)
        products = products.filter(category=subcategory)
        selected_category = subcategory.parent
        selected_subcategory = subcategory
    elif category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True, parent__isnull=True)
        # Get all subcategories of this category
        subcategories = Category.objects.filter(parent=category, is_active=True)
        # Get products from all subcategories
        products = products.filter(category__in=subcategories)
        selected_category = category
        selected_subcategory = None
    else:
        selected_category = None
        selected_subcategory = None
    
    return render(request, 'main/our-product.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'selected_subcategory': selected_subcategory,
    })
    
def productCategory(request, category_slug, subcategory_slug):
    # Top-level categories for menu
    categories = Category.objects.filter(parent__isnull=True, is_active=True).order_by('order')[:6]

    # Fetch parent and subcategory by slugs
    parent_category = get_object_or_404(Category, slug=category_slug, is_active=True, parent__isnull=True)
    subcategory = get_object_or_404(Category, slug=subcategory_slug, is_active=True, parent=parent_category)

    # Fetch products under the subcategory
    products = Product.objects.filter(is_active=True, category=subcategory).order_by('-id')

    featured = Product.objects.filter(is_active=True, featured=True, category=subcategory).order_by('-id')[:12]
    popular = Product.objects.filter(is_active=True, popular=True, category=subcategory).order_by('id')[:12]
    latest = Product.objects.filter(is_active=True, latest=True, category=subcategory).order_by('-id')[:12]

    return render(request, 'main/product-category.html', {
        'categories': categories,
        'parent_category': parent_category,
        'subcategory': subcategory,
        'products': products,
        'fl': featured,
        'pl': popular,
        'lts': latest,
    })
    
    
def contactus(request):
    categories = Category.objects.prefetch_related('subcategories').filter(parent__isnull=True)
    products = Product.objects.prefetch_related('images').all()
    return render(request, 'main/contact-us.html', {
        'categories': categories,
        'products': products
    })
def product_detail(request, slug):
    categories = Category.objects.filter(parent__isnull=True,is_active=True).order_by('order')[:6]
    product = get_object_or_404(Product.objects.prefetch_related('images', 'sections'), slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:5]  # limit to 5
    sections = product.sections.all()

    return render(request, 'jb/main/product-detail.html', {
        'product': product,
        'related_products': related_products,
        'sections': sections,
        'categories': categories,  # pass sections to template
        'footer': True,  # Show footer
    })

# def register(request):
    
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')

#         if password != confirm_password:
#             messages.error(request, "Passwords do not match.")
#             return redirect('register')

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#             return redirect('register')

#         user = User.objects.create_user(username=username, email=email, password=password)
#         login(request, user)
#         return redirect('home')

#     return render(request, 'main/register.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        date_of_birth = request.POST.get('date_of_birth')  # format: yyyy-mm-dd
        gender = request.POST.get('gender')
        profile_image = request.FILES.get('profile_image')

        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')

        # ✅ Generate username automatically
        if date_of_birth:
            dob_str = date_of_birth.replace('-', '')  # e.g., 19950512
        else:
            dob_str = '00000000'
        username = f"{first_name.lower()}{dob_str}"

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        if CustomUser.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number already exists.")
            return redirect('register')

        # Ensure username is unique
        original_username = username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{original_username}_{counter}"
            counter += 1

        user = CustomUser.objects.create(
            username=username,
            email=email,
            mobile=mobile,
            password=make_password(password),
            role='customer',
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth or None,
            gender=gender or None,
            profile_image=profile_image,
            address_line1=address_line1,
            address_line2=address_line2,
        )
        login(request, user)
        return redirect('home')

    return render(request, 'main/register.html')



def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))

    # Store product ID as key
    if str(product.id) in cart:
        cart[str(product.id)] += quantity
    else:
        cart[str(product.id)] = quantity

    request.session['cart'] = cart
    messages.success(request, f"{product.name} added to cart.")
    return redirect('product_detail', slug=product.slug)


def view_cart(request):
    categories = Category.objects.filter(parent__isnull=True,is_active=True).order_by('order')[:6]
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total_price += subtotal

    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'categories': categories,
        
    })


from django.views.decorators.csrf import csrf_exempt

@custom_login_required
def checkout(request):
    categories = Category.objects.filter(parent__isnull=True,is_active=True).order_by('order')[:6]
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total_price = 0
    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        cart_items.append({
            'categories': categories,
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total_price += subtotal

            # ✅ Get logged-in custom user from session
    user_id = request.session.get('custom_user_id')
    user = CustomUser.objects.filter(id=user_id).first() if user_id else None

    if request.method == 'POST':
        # Extract fields manually from POST
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code')
        city = request.POST.get('city')

        # Create and save the Order
        order = Order.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            postal_code=postal_code,
            city=city,
            paid=False
        )

        # Save Order Items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['product'].price,
                quantity=item['quantity']
            )

        # Clear the cart
        request.session['cart'] = {}
        messages.success(request, f'Order {order.id} placed successfully.')

        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'main/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'user': user,  # ✅ add this line

    })


@custom_login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'main/order_confirmation.html', {'order': order})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    return redirect('view_cart')


def update_cart_quantity(request, product_id):
    if request.method == "POST":
        new_quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if new_quantity > 0:
            cart[str(product_id)] = new_quantity
        else:
            del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, "Cart updated.")
    return redirect('view_cart')


def cart_item_count(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())
    return {'cart_item_count': total_items}


def custom_logout(request):
    logout(request)
    return redirect('home')


def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
            if check_password(password, user.password):
                # Store required info in session
                request.session['custom_user_id'] = user.id
                request.session['custom_user_email'] = user.email
                request.session['custom_user_name'] = user.username
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password")
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email or password")

    return render(request, 'main/login.html')


@custom_login_required
def profile_view(request):
    user_id = request.session.get('custom_user_id')
    if not user_id:
        return redirect('custom_login')

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect('custom_login')

    return render(request, 'main/profile.html', {'user': user})
    

def order_history(request):
    user_id = request.session.get('custom_user_id')
    user = CustomUser.objects.filter(id=user_id).first()

    if not user:
        messages.error(request, "Please log in to view your orders.")
        return redirect('login')  # or wherever your login page is

    orders = Order.objects.filter(user=user).order_by('-created')

    return render(request, 'main/order_history.html', {
        'orders': orders
    })


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            mobile=mobile,
            email=email,
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')  # replace with your actual route name

    return render(request, 'main/contact-us.html')



# News-News-search--------
# def find_post_by_title(request):
#     seo='allnews'
#     current_datetime = datetime.now()
#     events=NewsPost.objects.filter(Event=1,status='active').order_by('-id') [:10]
#     bp=BrandPartner.objects.filter(is_active=1).order_by('-id') [:20]
#     articales=NewsPost.objects.filter(schedule_date__lt=current_datetime,articles=1,status='active').order_by('-id') [:3]
#     vidarticales=VideoNews.objects.filter(articles=1,is_active='active',video_type='video').order_by('order')[:2]
#     headline=NewsPost.objects.filter(schedule_date__lt=current_datetime,Head_Lines=1,status='active').order_by('-id') [:14]
#     trending=NewsPost.objects.filter(schedule_date__lt=current_datetime,trending=1,status='active').order_by('-id') [:7]
#     brknews=NewsPost.objects.filter(BreakingNews=1,status='active').order_by('-id') [:8]
#     podcast=VideoNews.objects.filter(is_active='active').order_by('-id') [:2]
#     Category=category.objects.filter(cat_status='active').order_by('order') [:12]
    
#     # --------------ad-manage-meny--------------
#     adtlid=ad_category.objects.get(ads_cat_slug='topleft-600x80')
#     adtopleft=ad.objects.filter(ads_cat_id=adtlid.id, is_active=1).order_by('-id') [:1]
    
#     adtrid=ad_category.objects.get(ads_cat_slug='topright-600x80')
#     adtopright=ad.objects.filter(ads_cat_id=adtrid.id, is_active=1).order_by('-id') [:1]
    
#     adtopid=ad_category.objects.get(ads_cat_slug='leaderboard')
#     adtop=ad.objects.filter(ads_cat_id=adtopid.id, is_active=1).order_by('-id') [:1]
    
#     adleftid=ad_category.objects.get(ads_cat_slug='skyscraper')
#     adleft=ad.objects.filter(ads_cat_id=adleftid.id, is_active=1).order_by('-id') [:1]
    
#     adrcol=ad_category.objects.get(ads_cat_slug='mrec')
#     adright=ad.objects.filter(ads_cat_id=adrcol.id, is_active=1).order_by('-id') [:1]
    
#     festbg=ad_category.objects.get(ads_cat_slug='festivebg')
#     festive=ad.objects.filter(ads_cat_id=festbg.id, is_active=1).order_by('-id') [:1]
    
#     topad=ad_category.objects.get(ads_cat_slug='topad')
#     tophead=ad.objects.filter(ads_cat_id=topad.id, is_active=1).order_by('-id') [:1]
#     popup=ad_category.objects.get(ads_cat_slug='popup')
#     popupad=ad.objects.filter(ads_cat_id=popup.id, is_active=1).order_by('-id') [:1]
# # -------------end-ad-manage-meny--------------    

#     title = request.GET.get('title')
#     if title:
#         blogdata = NewsPost.objects.filter(post_title__contains=title,is_active=1,status='active')
#         if blogdata.exists():
#             data={
#                 'indseo':seo,
#                 'BlogData':blogdata,
#                 'event':events,
#                 'bplogo':bp,
#                 'Blogcat':Category,
#                 'adtop':adtop,
#                 'adleft':adleft,
#                 'adright':adright,
#                 'adtl':adtopleft,
#                 'adtr':adtopright,
#                 'bgad':festive,
#                 'headtopad':tophead,
#                 'popup':popupad,
#                 'Articale':articales,
#                 'vidart':vidarticales,
#                 'headline':headline,
#                 'bnews':brknews,
#                 'vidnews':podcast,
#                 'trendpost':trending,
#                 }
#             return render(request, 'all-news.html', data)
#         else:
#             data={
#                 'messages':'No Data Found!',
#                 }
#             return render(request, 'error.html', data)
#     else:
#         data={
#             'messages':'No Data Found!',
#             }
#         return render(request, 'error.html', data)
# News-News-search-end-------
