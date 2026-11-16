from django.db import migrations


DEFAULT_MALL_CATEGORIES = [
    ('Electronics', 'Smart devices, gadgets, and digital accessories for mall shoppers.'),
    ('Fashion & Apparel', 'Trending clothing, essentials, and premium everyday wear.'),
    ('Footwear', 'Shoes, sandals, and comfort-first footwear for every age.'),
    ('Home & Living', 'Home essentials, décor, and everyday living solutions.'),
    ('Grocery & Essentials', 'Daily groceries, pantry staples, and household necessities.'),
    ('Beauty & Personal Care', 'Skincare, grooming, and wellness products.'),
    ('Kids & Toys', 'Fun, educational, and playful items for children.'),
    ('Sports & Fitness', 'Fitness gear, accessories, and outdoor activity essentials.'),
    ('Pharmacy', 'Healthcare, wellness, and everyday medical care items.'),
    ('Jewelry & Accessories', 'Fashion gems, watches, and premium accessories.'),
]

DEFAULT_MALL_PRODUCTS = [
    ('Electronics', 'ELE-1001', 'Wireless Earbuds', 2499.00, 3599.00, 32, 12),
    ('Electronics', 'ELE-1002', 'Smart Watch Pro', 4599.00, 6999.00, 18, 8),
    ('Electronics', 'ELE-1003', 'USB-C Fast Charger', 799.00, 1299.00, 54, 15),
    ('Fashion & Apparel', 'FAS-2001', 'Cotton Premium Tee', 399.00, 699.00, 76, 20),
    ('Fashion & Apparel', 'FAS-2002', 'Classic Denim Jeans', 1199.00, 1899.00, 42, 12),
    ('Fashion & Apparel', 'FAS-2003', 'Lightweight Hoodie', 899.00, 1499.00, 35, 10),
    ('Footwear', 'FOO-3001', 'Running Shoes', 1699.00, 2499.00, 28, 10),
    ('Footwear', 'FOO-3002', 'Casual Sandals', 799.00, 1299.00, 41, 12),
    ('Home & Living', 'HOM-4001', 'LED Desk Lamp', 1099.00, 1799.00, 24, 8),
    ('Home & Living', 'HOM-4002', 'Premium Bedsheet Set', 1499.00, 2299.00, 20, 6),
    ('Grocery & Essentials', 'GRO-5001', 'Premium Rice 5kg', 549.00, 799.00, 64, 20),
    ('Grocery & Essentials', 'GRO-5002', 'Extra Virgin Olive Oil', 699.00, 999.00, 46, 15),
    ('Beauty & Personal Care', 'BEA-6001', 'Hydrating Face Serum', 899.00, 1499.00, 33, 10),
    ('Beauty & Personal Care', 'BEA-6002', 'Daily Hair Shampoo', 349.00, 599.00, 55, 18),
    ('Kids & Toys', 'KID-7001', 'Educational Learning Blocks', 699.00, 1199.00, 31, 10),
    ('Kids & Toys', 'KID-7002', 'Plush Teddy Bear', 499.00, 899.00, 38, 12),
    ('Sports & Fitness', 'SPO-8001', 'Yoga Mat', 849.00, 1499.00, 26, 8),
    ('Sports & Fitness', 'SPO-8002', 'Adjustable Dumbbell Set', 2399.00, 3999.00, 12, 5),
    ('Pharmacy', 'PHA-9001', 'Multivitamin Tablets', 399.00, 699.00, 52, 16),
    ('Pharmacy', 'PHA-9002', 'Hand Sanitizer 500ml', 159.00, 279.00, 88, 20),
    ('Jewelry & Accessories', 'JWL-10001', 'Silver Ring', 1899.00, 3299.00, 14, 5),
    ('Jewelry & Accessories', 'JWL-10002', 'Leather Wallet', 1199.00, 2199.00, 19, 6),
]


def add_default_categories(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    for name, description in DEFAULT_MALL_CATEGORIES:
        Category.objects.get_or_create(name=name, defaults={'description': description})


def add_default_products(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    Product = apps.get_model('products', 'Product')

    for category_name, product_code, product_name, purchase_price, selling_price, quantity, minimum_stock in DEFAULT_MALL_PRODUCTS:
        category = Category.objects.get(name=category_name)
        Product.objects.update_or_create(
            product_code=product_code,
            defaults={
                'name': product_name,
                'category': category,
                'purchase_price': purchase_price,
                'selling_price': selling_price,
                'quantity': quantity,
                'minimum_stock': minimum_stock,
            },
        )


def remove_default_products(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    codes = [code for _, code, _, _, _, _, _ in DEFAULT_MALL_PRODUCTS]
    Product.objects.filter(product_code__in=codes).delete()


def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    names = [name for name, _ in DEFAULT_MALL_CATEGORIES]
    Category.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_seed_mall_categories'),
    ]

    operations = [
        migrations.RunPython(add_default_categories, remove_default_categories),
        migrations.RunPython(add_default_products, remove_default_products),
    ]
