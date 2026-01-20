# Generated manually to make meta_title and meta_description required

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0013_populate_offer_meta_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='meta_description',
            field=models.CharField(max_length=255, verbose_name='Meta Description (SEO)'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='meta_title',
            field=models.CharField(max_length=160, verbose_name='Meta Title (SEO)'),
        ),
    ]

