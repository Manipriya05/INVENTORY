# Inventory Billing

A Django-based inventory and billing application with mall product categories, stock tracking, purchases, sales, customers, suppliers, and reports.

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and set a private `DJANGO_SECRET_KEY`.
4. Apply migrations and create an administrator:

   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. Start the development server:

   ```powershell
   python manage.py runserver
   ```

The local SQLite database is intentionally excluded from Git. Mall categories and sample products are created by the product migrations.
