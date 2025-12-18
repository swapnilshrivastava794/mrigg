# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0022_alter_customuser_options_alter_category_parent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariation',
            name='is_sku_code',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Is SKU Code'),
        ),
        migrations.AddField(
            model_name='productvariation',
            name='color_code',
            field=models.CharField(blank=True, max_length=7, null=True, verbose_name='Color Code'),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='unit',
            field=models.CharField(blank=True, choices=[('ml', 'ml'), ('l', 'L'), ('g', 'g'), ('kg', 'kg'), ('pcs', 'pcs'), ('pieces', 'pieces'), ('m', 'm'), ('cm', 'cm'), ('inch', 'inch'), ('ft', 'ft'), ('oz', 'oz'), ('lb', 'lb')], max_length=50, null=True, verbose_name='Unit'),
        ),
    ]

