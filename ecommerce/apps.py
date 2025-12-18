from django.apps import AppConfig


class EcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerce'
    verbose_name = 'Ecommerce'
    
    def ready(self):
        # Ensure app is properly configured
        pass