from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Q
from .models import CMS
from ecommerce.models import Category
from mriigproject import shopViews

# Create your views here.

def cms_page(request, slug):
    """
    View to display CMS pages by slug.
    If slug doesn't exist in CMS but exists as a category, route to shop view.
    """
    # First check if it's a CMS page
    try:
        cms_page = CMS.objects.get(slug=slug, status='active')
        
        # Increment view counter
        cms_page.viewcounter += 1
        cms_page.save(update_fields=['viewcounter'])
        
        return render(request, 'cms/page.html', {
            'cms_page': cms_page,
            'title': cms_page.pagename,
            'footer': True,
        })
    except CMS.DoesNotExist:
        # If not a CMS page, check if it's a category
        # If it's a category, route to shop view
        if Category.objects.filter(slug=slug, is_active=True).exists():
            return shopViews.shop(request, category_slug=slug)
        # If neither CMS nor category, raise 404
        raise Http404("Page not found")
