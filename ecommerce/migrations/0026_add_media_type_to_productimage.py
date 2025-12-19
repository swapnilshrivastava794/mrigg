# Generated manually to add media_type field to ProductImage

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0025_fix_brand_id_autoincrement'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='media_type',
            field=models.CharField(
                choices=[('image', 'Image'), ('video', 'Video')],
                default='image',
                max_length=10,
                verbose_name='Media Type'
            ),
        ),
    ]

