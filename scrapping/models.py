from django.db import models
from django.utils import timezone
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"
    
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.FloatField()
    offer_price = models.FloatField(default=0)
    rating = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name