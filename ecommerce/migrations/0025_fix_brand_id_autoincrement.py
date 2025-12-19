# Generated manually to fix AUTO_INCREMENT on Brand.id field

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0024_create_subcategory_and_update_product'),
    ]

    operations = [
        migrations.RunSQL(
            # Fix AUTO_INCREMENT on id column for main_brand table
            sql="ALTER TABLE `main_brand` MODIFY COLUMN `id` BIGINT AUTO_INCREMENT NOT NULL PRIMARY KEY;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]

