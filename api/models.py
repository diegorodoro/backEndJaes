from django.db import models
from django.core.validators import MinValueValidator

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    lote = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.nombre} ({self.sku})"

