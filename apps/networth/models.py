from django.db import models
from django.contrib.auth.models import User

ASSET_TYPES = [
        ('RES', 'Real Estate'),
        ('VEH', 'Vehicle'),
        ('STK', 'Stocks'),
        ('LUX', 'Luxury Item'),
        ('OTH', 'Other'),
    ]

class ManualAsset(models.Model):
    category = models.CharField(max_length=3, choices = ASSET_TYPES, default ='OTH')
    description = models.CharField(max_length = 400)
    current_value = models.DecimalField(max_digits=10,decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manual_assets")

    def __str__(self):
        return self.description

