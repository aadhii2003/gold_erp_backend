from django.db import models

class Sale(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    branch = models.ForeignKey('branches.Branch', on_delete=models.CASCADE, related_name='sales', null=True)
    staff = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    
    # RFQ Section
    vendor = models.CharField(max_length=255, blank=True, null=True)
    purchase_method = models.CharField(max_length=100, blank=True, null=True)
    market_price_currency = models.CharField(max_length=10, default='USD')
    market_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    discount_addition = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    net_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    market_price_unit = models.CharField(max_length=50, default='g')
    
    # Header Constants / Metadata
    order_deadline = models.DateField(null=True, blank=True)
    expected_arrival = models.DateField(null=True, blank=True)
    transaction_currency = models.CharField(max_length=10, default='USD')
    currency_rate = models.DecimalField(max_digits=15, decimal_places=4, default=1.0)
    transaction_unit = models.CharField(max_length=50, default='t')
    conversion_market_unit = models.DecimalField(max_digits=15, decimal_places=4, default=0.38)
    x_factor = models.DecimalField(max_digits=12, decimal_places=4, default=92.0)
    
    payment_ref = models.CharField(max_length=100, default='Paid Unfixed Amount')
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)

    # Product Table fields (Moved into model directly for Phase 1 simplicity)
    product_name = models.CharField(max_length=255, default="Gold Bar")
    description = models.TextField(blank=True, null=True)
    gross_weight = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    actual_process_weight = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    second_process_weight = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    process_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    density = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    actual_product_quality = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) # Purity
    
    manual_first_process = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    manual_purity = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    qty_tolas = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    tola_rate = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)

    unit_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    total_ugx = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id} - {self.vendor}"
