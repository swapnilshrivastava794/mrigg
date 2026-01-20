# Generated manually to make offer_image required

from django.db import migrations, models


def delete_offers_without_images(apps, schema_editor):
    """Delete offers that don't have images before making the field required"""
    Offer = apps.get_model('ecommerce', 'Offer')
    # Delete offers without images
    Offer.objects.filter(offer_image__isnull=True).delete()
    Offer.objects.filter(offer_image='').delete()


def reverse_delete_offers(apps, schema_editor):
    """Reverse migration - nothing to do as deleted offers can't be restored"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0015_alter_offer_options_offer_order'),
    ]

    operations = [
        # Delete offers without images first
        migrations.RunPython(delete_offers_without_images, reverse_delete_offers),
        
        # Make the field required
        migrations.AlterField(
            model_name='offer',
            name='offer_image',
            field=models.ImageField(upload_to='offers/', verbose_name='Offer Image'),
        ),
    ]

