from django.db.models import Prefetch
from ecommerce.models import CustomUser, Category


def cart_item_count(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())
    return {'cart_item_count': total_items}


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
    categories = Category.objects.filter(parent__isnull=True, is_active=True).order_by('order')[:6]
    # All categories with active subcategories for sidebar/menu
    all_categories = Category.objects.filter(
        parent__isnull=True, 
        is_active=True
    ).prefetch_related(
        Prefetch(
            'subcategories',
            queryset=Category.objects.filter(is_active=True).order_by('order')
        )
    ).order_by('order')
    return {
        'categories': categories,
        'all_categories': all_categories
    }