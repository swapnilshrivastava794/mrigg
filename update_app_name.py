#!/usr/bin/env python
"""
Script to update app name from 'main' to 'ecommerce' in database
Run this script: python update_app_name.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mriigproject.settings')
django.setup()

from django.db import connection

def update_app_name():
    with connection.cursor() as cursor:
        # Update django_content_type table
        cursor.execute("UPDATE django_content_type SET app_label = 'ecommerce' WHERE app_label = 'main'")
        content_type_count = cursor.rowcount
        
        # Update django_migrations table
        cursor.execute("UPDATE django_migrations SET app = 'ecommerce' WHERE app = 'main'")
        migrations_count = cursor.rowcount
        
        print(f"Updated {content_type_count} records in django_content_type")
        print(f"Updated {migrations_count} records in django_migrations")
        print("Database updated successfully!")

if __name__ == '__main__':
    update_app_name()

