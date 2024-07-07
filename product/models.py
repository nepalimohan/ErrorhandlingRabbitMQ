from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    product_type = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Product"
        ordering = ('-id',)
    
    def __str__(self):
        return self.name
    