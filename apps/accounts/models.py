import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg
from django.utils import timezone

MONTHS = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
              11: 'Nov', 12: 'Dec'}
def return_date_time():
    now = timezone.now()
    return now + datetime.timedelta(days=1)

INSTITUTION_CHOICES = [
        ('DES', 'Desjardins'),
        ('RBC', 'Royal Bank of Canada'),
        ('BNC', 'Banque Nationale'),
        ('VIE', 'Canada Vie'),
        ('SUN', 'Sun Life'),
    ]

TYPE_CHOICES = [
        ('CR', 'Credit'),
        ('DB', 'Debit')
    ] 

def get_total_account_value(accounts):
        
        total = 0
        for account in accounts:
            if account.type == 'CR':
                total = total - account.balance
            else:
                total = total + account.balance
        return total 

def get_institution_logo(institution_name):
    if institution_name == 'DES':
        return "/static/assets/img/banks/desjardins-logo.jpg"
    elif institution_name == 'RBC':
        return "/static/assets/img/banks/rbc-logo.jpg"
    elif institution_name == 'BNC':
        return "/static/assets/img/banks/bnc-logo.jpg"
    elif institution_name == 'VIE':
        return "/static/assets/img/banks/canadavie-logo.jpg"
    elif institution_name == 'SUN':
        return "/static/assets/img/banks/sunlife-logo.jpg"
    else:
        return "/static/assets/img/theme/bootstrap.jpg"   

class Institution(models.Model):
    name = models.CharField(max_length=3, choices = INSTITUTION_CHOICES, default ='DES')
    description = models.CharField(max_length = 400)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="institutions")

    def get_institution_logo(self):
        return get_institution_logo(self.name)
    
    def __str__(self):
        return self.get_name_display() + ' - ' + self.description
    
    def get_total_value(self):
        return get_total_account_value(self.accounts.all())
    
    def get_account_count(self):
        q = self.objects.select_related('accounts').annotate(num_B=Count('accounts'))
        return self.num_B
    
    def get_accounts(self):
        return self.accounts.all()

class Desjardins(Institution):
    security_questions_1=models.TextField()
    security_answer_1=models.CharField(max_length=50)
    security_questions_2=models.TextField()
    security_answer_2=models.CharField(max_length=50)
    security_questions_3=models.TextField()
    security_answer_3=models.CharField(max_length=50)

class Account(models.Model):
    number = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    balance = models.DecimalField(max_digits=10,decimal_places=2)
    type = models.CharField(max_length=2, choices = TYPE_CHOICES, default = 'DB')
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    parent_institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="accounts")

    def get_balance(self):
        return self.account_values.latest().value

    def __str__(self):
        return self.parent_institution.get_name_display() + ' - ' + self.number
    
    def save(self, commit=True): 
        obj = super().save()
        
        self.parent_institution.save()
        return obj
    
    def account_over_time_report(self):
        now = datetime.datetime.now()

        month_val = now.month + 1

        # Limit the upper value
        if month_val > 12:
            month_val = 12
        
        filter_params = {
            'value_date__gte': '{year}-{month}-{day}'.format(year=now.year - 1, month=month_val,
                                                                     day=now.day),
            'value_date__lte': now.date()
        }

        annotate_params = {
            'average_value': Avg('value_float')
        }

        objects = self.values.all()
        filtered_obj = objects.filter(**filter_params)
        queryset = filtered_obj.values('value_date__year', 'value_date__month').annotate(**annotate_params)

        return list(queryset), [MONTHS[data.get('value_date__month')] for data in queryset]


    class Meta:
        get_latest_by = "last_updated"

class AccountValue(models.Model):
    value = models.DecimalField(max_digits=10,decimal_places=2)
    value_date = models.DateField(default=return_date_time)
    value_float = models.FloatField(default=10)
    last_updated = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="values")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_values")

    def save(self, commit=True): 
        self.value_float = float(self.value)
        obj = super().save()
        self.account.balance = self.value
        self.account.save()
        return obj
    
    class Meta:
        get_latest_by = "value_date"