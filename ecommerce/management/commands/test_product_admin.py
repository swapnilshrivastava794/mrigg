"""
Management command to test ProductAdmin performance and generate diagnostic logs
Usage: python manage.py test_product_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.admin.sites import site
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from ecommerce.models import Product
from ecommerce.admin import ProductAdmin
import time
import logging
from django.db import connection, reset_queries

logger = logging.getLogger('ecommerce.admin')
User = get_user_model()


class Command(BaseCommand):
    help = 'Test ProductAdmin performance and generate diagnostic logs'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== ProductAdmin Performance Test ===\n'))
        
        # Reset queries
        reset_queries()
        
        # Create a mock request
        factory = RequestFactory()
        request = factory.get('/admin/ecommerce/product/')
        
        # Get a superuser or create one for testing
        try:
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                self.stdout.write(self.style.WARNING('No superuser found. Creating test user...'))
                user = User.objects.create_user(
                    username='test_admin',
                    email='test@test.com',
                    password='test123',
                    is_superuser=True,
                    is_staff=True
                )
            request.user = user
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {e}'))
            return
        
        # Get ProductAdmin instance
        product_admin = ProductAdmin(Product, site)
        
        # Test 1: Get queryset
        self.stdout.write('\n1. Testing get_queryset()...')
        start_time = time.time()
        try:
            qs = product_admin.get_queryset(request)
            count = qs.count()
            elapsed = time.time() - start_time
            self.stdout.write(self.style.SUCCESS(f'   ✓ Queryset created: {count} products in {elapsed:.3f}s'))
            self.stdout.write(f'   Queries executed: {len(connection.queries)}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Error: {e}'))
            logger.error(f'Error in get_queryset: {e}', exc_info=True)
            return
        
        # Test 2: Get first 50 products
        self.stdout.write('\n2. Testing fetching first 50 products...')
        reset_queries()
        start_time = time.time()
        try:
            products = list(qs[:50])
            elapsed = time.time() - start_time
            self.stdout.write(self.style.SUCCESS(f'   ✓ Fetched {len(products)} products in {elapsed:.3f}s'))
            self.stdout.write(f'   Queries executed: {len(connection.queries)}')
            
            if len(connection.queries) > 5:
                self.stdout.write(self.style.WARNING(f'   ⚠ Too many queries! Expected < 5, got {len(connection.queries)}'))
                for i, query in enumerate(connection.queries[:10], 1):
                    self.stdout.write(f'   Query {i}: {query["sql"][:100]}... (Time: {query["time"]}s)')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Error: {e}'))
            logger.error(f'Error fetching products: {e}', exc_info=True)
        
        # Test 3: Test inlines
        self.stdout.write('\n3. Testing inline querysets...')
        if products:
            test_product = products[0]
            reset_queries()
            start_time = time.time()
            try:
                # Test ProductImageInline
                from ecommerce.admin import ProductImageInline
                image_inline = ProductImageInline(Product, site)
                image_qs = image_inline.get_queryset(request).filter(product=test_product)
                image_count = image_qs.count()
                
                # Test ProductVariationInline
                from ecommerce.admin import ProductVariationInline
                variation_inline = ProductVariationInline(Product, site)
                variation_qs = variation_inline.get_queryset(request).filter(product=test_product)
                variation_count = variation_qs.count()
                
                # Test ProductSectionInline
                from ecommerce.admin import ProductSectionInline
                section_inline = ProductSectionInline(Product, site)
                section_qs = section_inline.get_queryset(request).filter(product=test_product)
                section_count = section_qs.count()
                
                elapsed = time.time() - start_time
                self.stdout.write(self.style.SUCCESS(f'   ✓ Inline querysets tested in {elapsed:.3f}s'))
                self.stdout.write(f'   Product: {test_product.name}')
                self.stdout.write(f'   Images: {image_count}, Variations: {variation_count}, Sections: {section_count}')
                self.stdout.write(f'   Queries executed: {len(connection.queries)}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   ✗ Error: {e}'))
                logger.error(f'Error testing inlines: {e}', exc_info=True)
        
        # Test 4: Database statistics
        self.stdout.write('\n4. Database Statistics...')
        try:
            total_products = Product.objects.count()
            products_with_images = Product.objects.filter(images__isnull=False).distinct().count()
            products_with_variations = Product.objects.filter(variations__isnull=False).distinct().count()
            products_with_sections = Product.objects.filter(sections__isnull=False).distinct().count()
            
            self.stdout.write(f'   Total Products: {total_products}')
            self.stdout.write(f'   Products with Images: {products_with_images}')
            self.stdout.write(f'   Products with Variations: {products_with_variations}')
            self.stdout.write(f'   Products with Sections: {products_with_sections}')
            
            if total_products > 1000:
                self.stdout.write(self.style.WARNING(f'   ⚠ Large dataset! Consider adding filters or pagination.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Error: {e}'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Test Complete ==='))
        self.stdout.write('\nCheck logs/admin_debug.log for detailed information.')

