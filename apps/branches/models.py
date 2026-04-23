from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    x_factor = models.DecimalField(max_digits=12, decimal_places=4, default=92.0000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (X: {self.x_factor})"

class UOM(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=[
        ('smaller', 'Smaller than reference'),
        ('reference', 'Reference Unit'),
        ('bigger', 'Bigger than reference')
    ])

    def __str__(self):
        return f"{self.name} ({self.code})"

class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code

class Expense(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='expenses')
    source_name = models.CharField(max_length=255)
    rate_per_gram = models.DecimalField(max_digits=12, decimal_places=2)
    grams = models.DecimalField(max_digits=12, decimal_places=4)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_name} - {self.total} ({self.branch.name})"
