from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()

    def __str__(self):
        return self.name