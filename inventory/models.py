
from django.db import models
class StockMovement(models.Model):
    MOVEMENT_CHOICES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJUSTMENT', 'Stock Adjustment'),
    ]
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE
    )
    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_CHOICES
    )
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    def __str__(self):
        return f"{self.product.name} - {self.movement_type}"
