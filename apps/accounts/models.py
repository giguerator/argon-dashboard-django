from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

from apps.core_assets.models import Asset

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
                total = total - account.current_value
            else:
                total = total + account.current_value
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
        try:
            account_count = len(self.accounts)
        except:
            return 0
        return account_count
    
    def get_accounts(self):
        return self.accounts.all()

class Desjardins(Institution):
    security_questions_1=models.TextField()
    security_answer_1=models.CharField(max_length=50)
    security_questions_2=models.TextField()
    security_answer_2=models.CharField(max_length=50)
    security_questions_3=models.TextField()
    security_answer_3=models.CharField(max_length=50)

class Account(Asset, models.Model):
    number = models.CharField(max_length=64)
    type = models.CharField(max_length=2, choices = TYPE_CHOICES, default = 'DB')
    parent_institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="accounts")
    user_child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')


    def __str__(self):
        return self.parent_institution.get_name_display() + ' - ' + self.number
    
    def save(self, *args, **kwargs): 
        obj = super().save( *args, **kwargs)
        
        self.parent_institution.save()
        return obj