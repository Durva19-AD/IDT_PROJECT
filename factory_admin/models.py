from django.db import models

class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price_per_unit = models.FloatField()
    
    def __str__(self):
        return f"{self.name} - ₹{self.price_per_unit}"

class Inventory(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='inventory_records')
    quantity = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.material.name} - {self.quantity} units"


class DimensionConfig(models.Model):
    DESIGN_CHOICES = [
        ('window', 'Window'),
        ('door', 'Door'),
    ]
    design_type = models.CharField(max_length=20, unique=True, choices=DESIGN_CHOICES)
    min_width = models.FloatField(default=300)
    max_width = models.FloatField(default=3000)
    min_height = models.FloatField(default=300)
    max_height = models.FloatField(default=3000)

    def __str__(self):
        return f"{self.get_design_type_display()} Config"

