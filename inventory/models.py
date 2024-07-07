from django.db import models

# Create your models here.
class Inventory(models.Model):
    product_id = models.IntegerField()
    total_quantity = models.IntegerField()
    
    class Meta:
        ordering = ('-id',)
    