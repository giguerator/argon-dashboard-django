import datetime

from apps.accounts.models import Account, AccountValue
from random import random
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Populate account values to create a dummy project"

    def handle(self, *args, **options):
        number_of_samples = 100
        initial_balance_max = 10000
        transaction_max = 1000
        initial_date = datetime.datetime(year=2022, month=1, day=1)
        end_date = datetime.datetime(year=2024, month=1, day=1)
        timestep = (end_date - initial_date)/number_of_samples

        for account in Account.objects.all():
            value = initial_balance_max * random()
            value_date=initial_date
            for i in range(number_of_samples):
                account_value = AccountValue(user = account.user, value = value, value_date = value_date, account = account)
                value = value + ((random() > 0.5 ) * -1) * transaction_max * random()
                value_date = value_date + timestep
                account_value.save()
            
            self.stdout.write(
                self.style.SUCCESS('Successfully created account values for  "%s"' % account.number)
            ) 


            