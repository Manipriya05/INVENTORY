from django.db import migrations


DEFAULT_MALL_CATEGORIES = [
    ('Electronics', 'Phones, laptops, audio, and digital accessories.'),
    ('Fashion & Apparel', 'Clothing, uniforms, and daily wear for shoppers.'),
    ('Footwear', 'Shoes, sandals, and accessories for all ages.'),
    ('Home & Living', 'Furniture, décor, and home essentials.'),
    ('Grocery & Essentials', 'Daily groceries, packaged goods, and essentials.'),
    ('Beauty & Personal Care', 'Cosmetics, skincare, grooming, and care products.'),
    ('Kids & Toys', 'Children’s products, educational toys, and play essentials.'),
    ('Sports & Fitness', 'Athletic gear, fitness products, and outdoor essentials.'),
    ('Pharmacy', 'Health, wellness, and personal medical supplies.'),
    ('Jewelry & Accessories', 'Watches, gold, silver, and fashion accessories.'),
]


def add_default_categories(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    for name, description in DEFAULT_MALL_CATEGORIES:
        Category.objects.get_or_create(name=name, defaults={'description': description})


def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    names = [name for name, _ in DEFAULT_MALL_CATEGORIES]
    Category.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_category'),
    ]

    operations = [
        migrations.RunPython(add_default_categories, remove_default_categories),
    ]
