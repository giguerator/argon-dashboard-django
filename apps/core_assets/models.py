from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from django.db.models import Avg, Sum
import calendar
import datetime
import re
from itertools import chain

def month_delta(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

MONTHS = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
              11: 'Nov', 12: 'Dec'}

def return_date_time():
    now = timezone.now()
    return now + datetime.timedelta(days=1)

class Asset(models.Model):
    description = models.CharField(max_length=400)
    current_value = models.DecimalField(max_digits=10,decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assets")
    child_class = models.CharField(max_length=100, default='Asset')
    
    def get_current_value(self):
        return self.asset_values.latest().value

    def __str__(self):
        return self.description
    
    def save(self, commit=True):
        self.child_class = type(self).__name__
        obj = super().save()
        
        return obj
    
    def value_over_time_report(self, period='1y'):
        now = datetime.date.today()

        value_objects = self.object.asset_values.all()

        span = re.findall(r'[a-z]', period)[0]

        if period == 'max':
            initial_date = value_objects.earliest('value_date').value_date

        else:
            length = int(re.findall(r'[0-9]', period)[0])
            if span == 'm':
                initial_date = month_delta(now, -1*length)
            elif span == 'w':
                delta_date = datetime.timedelta(weeks=length)
                initial_date = now - delta_date
            elif span == 'd':
                delta_date = datetime.timedelta(days=length)
                initial_date = now - delta_date
            else:
                delta_date = datetime.timedelta(days=365)
                initial_date = now - delta_date * length
        
        filter_params = {
            'value_date__gte': initial_date,
            'value_date__lte': now
        }

        annotate_params = {
            'average_value': Avg('value_float')
        }

        filtered_obj = value_objects.filter(**filter_params)
        queryset = filtered_obj.values('value_date__year', 'value_date__month').annotate(**annotate_params)
        
        interval = now - initial_date

        if interval > 4*datetime.timedelta(days=365):
            labels=[str(data.get('value_date__year')) for data in queryset]
        elif interval > datetime.timedelta(days=365):
            labels=[MONTHS[data.get('value_date__month')] + "-" + str(data.get('value_date__year') )for data in queryset]
        elif interval > datetime.timedelta(days=31):
            labels=[MONTHS[data.get('value_date__month')] for data in queryset]
        else:
            queryset = filtered_obj.values('value_date').annotate(**annotate_params)
            labels=[str(data.get('value_date')) for data in queryset]

        return queryset, labels
    
    def combine_reports_over_time(querysets):
        result_list = AssetValue.objects.none()
        for list in querysets:
            result_list = list | result_list
        annotate_params = {
            'average_value': Sum('value_float')
        }
        queryset = result_list.annotate(**annotate_params)
        labels=[str(data.get('value_date')) for data in queryset]
        return queryset, labels
    
    class Meta:
        get_latest_by = "last_updated"

class AssetValue(models.Model):
     value_string = models.DecimalField(max_digits=10,decimal_places=2)
     value_date = models.DateField(default=return_date_time)
     value_float = models.FloatField(default=10)
     last_updated = models.DateTimeField(auto_now_add=True)
     asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="asset_values")
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="asset_values")

     def save(self, commit=True): 
         self.value_float = float(self.value_string)
         obj = super().save()
         self.asset.current_value = self.value_string
         self.asset.save()
         return obj
    
     class Meta:
         get_latest_by = "value_date"