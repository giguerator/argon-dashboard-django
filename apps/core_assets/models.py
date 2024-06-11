from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from django.db.models import Avg, Sum, F
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')
    child_class = models.CharField(max_length=100, default='Asset')
    
    def get_current_value(self):
        return self.asset_values.latest().value

    @staticmethod
    def get_total_asset_value(assets):
        total = 0
        for asset in assets:
            total = total + asset.current_value
        return total 

    def __str__(self):
        return self.description
    
    def save(self, commit=True):
        self.child_class = type(self).__name__
        obj = super().save()
        
        return obj        

    @staticmethod
    def __get_label_dates(start_date, end_date, resolution="1m"):
        span = re.findall(r'[a-z]', resolution)[0]
        length = int(re.findall(r'[0-9]', resolution)[0])

        if span == 'm':
            period_count = (end_date.month - start_date.month + (end_date.year - start_date.year) * 12) // length + 1
        if span == 'd':
            period_count = (end_date - start_date).days + 1

        label_dates=[]
        for time_period_itr in range(period_count):
            if span == 'm':
                label_date = month_delta(end_date, -time_period_itr*length) 
            if span == 'd':
                label_date = end_date - datetime.timedelta(days=-1) * time_period_itr
            label_dates = [label_date]+label_dates
        return label_dates

    @staticmethod
    def __match_date(data,date):
        try:
            condition = data['value_date']==date
        except:
            condition = data['value_date__month']==date.month and data['value_date__year']==date.year
        if condition:
            return True
        return False

    @staticmethod
    def __extrapolate_intrapolate_report(report, expected_dates):
        for index, expected_date in enumerate(expected_dates):
            element = list(filter(
                lambda data: Asset.__match_date(data, expected_date),
                report
            ))
            if not element:
                previous_element = list(filter(
                    lambda data: Asset.__match_date(data, expected_dates[index-1]),
                    report
                ))
                next_index = report.index(previous_element)+1

                try:
                    next_element = report[next_index]
                except:
                    next_element = previous_element
                if 'value_date__month' in report[0]:
                    new_element = {'value_date__year':expected_date.year, 'value_date__month':expected_date.month, 'average_value':(next_element['average_value']-previous_element['average_value'])/2}
                else:
                    new_element = {'value_date':expected_date, 'average_value':(next_element['average_value']-previous_element['average_value'])/2}

                report.insert(next_element)

                return report


    def value_over_time_report(self, period='1y'):
        now = datetime.date.today()

        value_objects = self.asset_values.all()

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

        if interval > datetime.timedelta(days=31):
            labels=[MONTHS[data.get('value_date__month')] + "-" + str(data.get('value_date__year')) for data in queryset]

        else:
            queryset = filtered_obj.values('value_date__year', 'value_date__month', 'value_date__day').annotate(**annotate_params)
            labels=[str(data.get('value_date__day')) + "-" + MONTHS[data.get('value_date__month')] + "-" + str(data.get('value_date__year')) for data in queryset]

        return list(queryset), labels
    
    @staticmethod
    def __match_date(data,month,year):
        if data['value_date__month']==month and data['value_date__year']==year:
            return True
        return False
    
    @staticmethod
    def __match_lower_than_date(data,month,year):
        if data['value_date__month']<month and data['value_date__year']<=year:
            return True
        return False

    @staticmethod
    def multi_asset_value_over_time_report(assets, period='1y'):
        
        report = None
        report_labels = None
        asset_report_labels = None
        for asset in assets:
            asset_report, asset_report_labels = asset.value_over_time_report(period=period)
        
            if report is None:
                report = asset_report
            else:
                for asset_report_item in asset_report:
                    matching_report = list(filter(
                        lambda data: Asset.__match_date(data, asset_report_item['value_date__month'],asset_report_item['value_date__year']),
                        report
                    ))

                    if 'average_value' not in matching_report[0]:
                        less_than_report = list(filter(
                        lambda data: Asset.__match_lower_than_date(data, asset_report_item['value_date__month'],asset_report_item['value_date__year']),
                        report
                    ))
                        report.insert(len(less_than_report),asset_report_item)

                previous_asset = None
                for report_item in report:
                    matching_asset_report = list(filter(
                        lambda data: Asset.__match_date(data, report_item['value_date__month'],report_item['value_date__year']),
                        asset_report
                    ))
                    if 'average_value' in matching_asset_report:
                        report_item['average_value'] += matching_asset_report[0]['average_value']
                        previous_asset = matching_asset_report
                    else:
                        if previous_asset is not None:
                            report_item['average_value'] += previous_asset['average_value']
            
        if report is not None:
            if 'value_date__day' in asset_report_labels[0]:
                report_labels=[str(data.get('value_date__day')) + "-" + MONTHS[data.get('value_date__month')] + "-" + str(data.get('value_date__year')) for data in report]
            
            else:
                report_labels=[MONTHS[data.get('value_date__month')] + "-" + str(data.get('value_date__year')) for data in report]

        return report, report_labels 
    
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