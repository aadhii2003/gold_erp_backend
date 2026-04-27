from django.db import models

class DensityPurity(models.Model):
    density = models.DecimalField(max_digits=5, decimal_places=2, unique=True)
    purity = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.density} -> {self.purity}%"
