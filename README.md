# Inventory Billing Management System

A Django-based inventory and billing application designed to manage product categories, stock tracking, purchases, sales, customers, suppliers, and business reports efficiently.

## 🚀 Project Overview

This application helps manage inventory and billing operations through a centralized web-based system.

## ✨ Key Features

- Product and Category Management
- Stock Tracking
- Purchase Management
- Sales Management
- Customer Management
- Supplier Management
- Billing and Invoices
- Business Reports
- Dashboard

## 🛠️ Technologies Used

- Python
- Django
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- SQLite

## 📂 Project Modules
- Accounts
- Dashboard
- Products
- Inventory
- Purchases
- Sales
- Customers
- Suppliers

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Manipriya05/INVENTORY.git
```

### 2. Navigate to the project folder

```bash
cd INVENTORY
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Configure environment variables

Copy `.env.example` to `.env` and set a private `DJANGO_SECRET_KEY`.

### 7. Apply migrations

```bash
python manage.py migrate
```

### 8. Create an administrator

```bash
python manage.py createsuperuser
```

### 9. Start the development server

```bash
python manage.py runserver
```

Open your browser:

`http://127.0.0.1:8000/`

## 🚀 Deploy on Render

This is a Django application, so it needs a Python web service and a persistent
database. The included `render.yaml` configures a Render web service and
PostgreSQL database.

1. Push the project to GitHub. Do not commit `.env` or `db.sqlite3`.
2. In Render, choose **New → Blueprint**, connect the GitHub repository, and
   apply the `render.yaml` blueprint. Render will create the web service and
   database; the service applies database migrations on startup.
3. Wait for the first deploy to finish, then open the web service's **Shell**
   and run `python manage.py createsuperuser` to create your login. Shell access
   may require a paid instance; if it is unavailable on your plan, temporarily
   switch to a plan that provides it.
4. Open the service URL shown by Render.

The local SQLite database is not copied to Render. The deployed PostgreSQL
database starts with the project's migrations and seeded sample products. If
you use a custom domain, add it to `DJANGO_ALLOWED_HOSTS` and add its HTTPS
origin to `DJANGO_CSRF_TRUSTED_ORIGINS` in the Render service's environment.
The included free plans may have usage or expiration limits; check Render's
current plan details before relying on them for business data.

## 🔒 Security

- Local SQLite database is excluded from Git.
- Private environment variables should not be uploaded to GitHub.
- Use a private Django secret key.

## 👩‍💻 Developer

**Manipriya**

B.Sc Computer Science | Junior Web Developer

GitHub: [Manipriya05](https://github.com/Manipriya05)

---

⭐ Thank you for visiting my project!
The local SQLite database is intentionally excluded from Git. Mall categories and sample products are created by the product migrations.

## Project Documentation
Inventory Billing Management System built using Django and Python.
d4e39dd (Improve README documentation)
