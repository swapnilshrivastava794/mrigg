# Generated manually to populate existing NULL meta fields

from django.db import migrations
from django.utils.html import strip_tags


def populate_meta_fields(apps, schema_editor):
    """Populate meta_title and meta_description from offer_title and offer_description"""
    Offer = apps.get_model('ecommerce', 'Offer')
    
    for offer in Offer.objects.all():
        # Populate meta_title if empty
        if not offer.meta_title or (offer.meta_title and not offer.meta_title.strip()):
            if offer.offer_title and offer.offer_title.strip():
                offer.meta_title = offer.offer_title[:160].strip()
            else:
                offer.meta_title = "Offer"  # Fallback default
        
        # Populate meta_description if empty
        if not offer.meta_description or (offer.meta_description and not offer.meta_description.strip()):
            if offer.offer_description and offer.offer_description.strip():
                clean_text = strip_tags(offer.offer_description)
                if clean_text and clean_text.strip():
                    offer.meta_description = clean_text[:255].strip()
                elif offer.offer_title and offer.offer_title.strip():
                    offer.meta_description = offer.offer_title[:255].strip()
                else:
                    offer.meta_description = "Special Offer"  # Fallback default
            elif offer.offer_title and offer.offer_title.strip():
                offer.meta_description = offer.offer_title[:255].strip()
            else:
                offer.meta_description = "Special Offer"  # Fallback default
        
        offer.save()


def reverse_populate_meta_fields(apps, schema_editor):
    """Reverse migration - set fields back to empty"""
    Offer = apps.get_model('ecommerce', 'Offer')
    Offer.objects.all().update(meta_title=None, meta_description=None)


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0012_offerproduct'),
    ]

    operations = [
        migrations.RunPython(populate_meta_fields, reverse_populate_meta_fields),
    ]

