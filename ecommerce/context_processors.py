from django.db.models import Prefetch
from ecommerce.models import CustomUser, Category, SubCategory, Brand, Product
from cms.models import profile_setting, CMS


def cart_item_count(request):
    """
    Context processor to provide cart and wishlist counts to all templates.
    Also provides cart items with product details for cart sidebar.
    Handles edge cases and ensures valid integer values.
    """
    cart_items = []
    total_items = 0
    cart_total_price = 0
    
    try:
        cart = request.session.get('cart', {})
        if not cart or not isinstance(cart, dict):
            cart = {}
        
        # Ensure all cart values are integers and calculate total items
        for key, value in cart.items():
            try:
                quantity = int(value) if value else 0
                total_items += quantity
            except (ValueError, TypeError):
                # Skip invalid values
                continue
        
        # Fetch cart items with product details if cart is not empty
        if cart:
            try:
                product_ids = [int(pid) for pid in cart.keys() if pid.isdigit()]
                if product_ids:
                    products = Product.objects.filter(
                        id__in=product_ids,
                        is_active=True
                    ).select_related('subcategory', 'subcategory__category').prefetch_related('images')
                    
                    for product in products:
                        product_id_str = str(product.id)
                        if product_id_str in cart:
                            quantity = int(cart[product_id_str])
                            # Get first product image
                            product_image = product.images.filter(media_type='image').first()
                            # Calculate effective price
                            effective_price = product.offerprice if product.offerprice and product.offerprice > 0 else product.price
                            subtotal = effective_price * quantity
                            cart_total_price += subtotal
                            
                            cart_items.append({
                                'product': product,
                                'quantity': quantity,
                                'subtotal': subtotal,
                                'effective_price': effective_price,
                                'product_image': product_image,
                            })
            except Exception as e:
                # If there's an error fetching products, just return empty list
                cart_items = []
    except Exception:
        total_items = 0
        cart_items = []
    
    try:
        wishlist = request.session.get('wishlist', [])
        if not isinstance(wishlist, list):
            wishlist = []
        wishlist_count = len(wishlist)
    except Exception:
        wishlist_count = 0
    
    return {
        'cart_item_count': total_items,
        'wishlist_count': wishlist_count,
        'cart_items': cart_items,
        'cart_total_price': cart_total_price,
    }


def custom_user_context(request):
    user = None
    user_id = request.session.get('custom_user_id')
    if user_id:
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            pass
    return {'custom_user': user}


def categories_context(request):
    # Get main categories (no parent field now)
    categories = Category.objects.filter(is_active=True).order_by('order')[:6]
    # All categories with active subcategories for sidebar/menu
    all_categories = Category.objects.filter(
        is_active=True
    ).prefetch_related(
        Prefetch(
            'subcategories',
            queryset=SubCategory.objects.filter(is_active=True).order_by('order')
        )
    ).order_by('order')
    
    # Get all active brands for menu dropdown
    all_brands = Brand.objects.filter(is_active=True).order_by('order', 'name')
    
    return {
        'categories': categories,
        'all_categories': all_categories,
        'all_brands': all_brands
    }


def profile_setting_context(request):
    """
    Context processor to provide profile_setting data to all templates.
    Returns the active profile_setting instance or None if not found.
    Also provides all active CMS entries for footer links.
    """
    try:
        profile = profile_setting.objects.filter(status='active').first()
    except Exception:
        profile = None
    
    try:
        # Get all active CMS entries ordered by order field
        cms_links = CMS.objects.filter(status='active').order_by('order', 'pagename')
    except Exception:
        cms_links = []
    
    return {
        'profile_setting': profile,
        'cms_links': cms_links,
    }