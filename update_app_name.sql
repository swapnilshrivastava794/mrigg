-- Update app name from 'main' to 'ecommerce' in database
UPDATE django_content_type SET app_label = 'ecommerce' WHERE app_label = 'main';
UPDATE django_migrations SET app = 'ecommerce' WHERE app = 'main';

