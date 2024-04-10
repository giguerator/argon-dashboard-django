from django.db import models
from django.contrib.auth.models import User
import datetime

from apps.core_assets.models import AssetValue, Asset

ASSET_TYPES = [
        ('RES', 'Real Estate'),
        ('VEH', 'Vehicle'),
        ('STK', 'Stocks'),
        ('LUX', 'Luxury Item'),
        ('OTH', 'Other'),
    ]

class ManualAsset(Asset, models.Model):
    category = models.CharField(max_length=3, choices = ASSET_TYPES, default ='OTH')
    user_child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manual_assets')

    def save(self, commit=True):
        asset_value = AssetValue(user = self.user, value_string = self.current_value, value_date = datetime.date.today(), asset = self)
        obj=super().save()
        return obj

