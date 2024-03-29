from django.test import TestCase

from models import Account, AccountValue
from random import random



number_of_samples = 100
initial_balance_max = 10000
transaction_max = 1000

for account in Account.objects.all():
    value = initial_balance_max * random()

    for i in range(number_of_samples):
        account_value = AccountValue(value=value,account=account)
        value = value + ((random() > 0.5 ) * -1) * transaction_max * random() 