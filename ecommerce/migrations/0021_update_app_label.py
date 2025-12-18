# Generated manually to update app_label from 'main' to 'ecommerce'

from django.db import migrations


def update_app_label_forward(apps, schema_editor):
    """Update app_label in django_content_type and django_migrations"""
    db_alias = schema_editor.connection.alias
    
    # Update django_content_type table
    schema_editor.execute("""
        UPDATE django_content_type 
        SET app_label = 'ecommerce' 
        WHERE app_label = 'main'
    """)
    
    # Update django_migrations table
    schema_editor.execute("""
        UPDATE django_migrations 
        SET app = 'ecommerce' 
        WHERE app = 'main'
    """)


def update_app_label_reverse(apps, schema_editor):
    """Reverse: change back to 'main'"""
    db_alias = schema_editor.connection.alias
    
    schema_editor.execute("""
        UPDATE django_content_type 
        SET app_label = 'main' 
        WHERE app_label = 'ecommerce'
    """)
    
    schema_editor.execute("""
        UPDATE django_migrations 
        SET app = 'main' 
        WHERE app = 'ecommerce'
    """)


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0020_productvariation_quantity_productvariation_unit_and_more'),
    ]

    operations = [
        migrations.RunPython(update_app_label_forward, update_app_label_reverse),
    ]

