# Generated manually for SubCategory model and Product.category to subcategory change

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0023_productvariation_is_sku_code_productvariation_color_code_alter_productvariation_unit'),
    ]

    operations = [
        # Create SubCategory model
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='subcategories/%Y/%m/%d', verbose_name='SubCategory Image')),
                ('is_active', models.BooleanField(default=True, verbose_name='Status')),
                ('order', models.IntegerField(blank=True, default=None, null=True, verbose_name='Order')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='ecommerce.category', verbose_name='Main Category')),
            ],
            options={
                'verbose_name_plural': 'SubCategories',
                'db_table': 'main_subcategory',
                'ordering': ['category__order', 'category__name', 'order', 'name'],
            },
        ),
        migrations.AddConstraint(
            model_name='subcategory',
            constraint=models.UniqueConstraint(fields=('category', 'slug'), name='unique_category_slug'),
        ),
        # Add subcategory field to Product (nullable first for data migration)
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='ecommerce.subcategory', verbose_name='SubCategory'),
        ),
        # Note: Remove old category field in next migration after data migration
    ]

