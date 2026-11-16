
from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=150)
    product_code = models.CharField(max_length=50, unique=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(default=0)
    minimum_stock = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name
