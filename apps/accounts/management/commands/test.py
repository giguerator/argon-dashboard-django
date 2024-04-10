import datetime

from apps.accounts.models import Account, Institution
from apps.core_assets.models import Asset,AssetValue
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Avg, Sum
from django.db.models import Q

from itertools import chain

def match_date(data,month,year):
    if data['value_date__month']==month and data['value_date__year']==year:
        return True
    return False

class Command(BaseCommand):
    help = "Test"

    def handle(self, *args, **options):
        asset1 ,labels1 = Asset.objects.get(pk=21).value_over_time_report()
        asset2 ,labels2 = Asset.objects.get(pk=22).value_over_time_report()
        assets = Asset.objects.filter(Q(pk=21)|Q(pk=22))
        report, labels = Asset.multi_asset_value_over_time_report(assets)

        print('a')