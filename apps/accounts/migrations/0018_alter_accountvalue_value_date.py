# Generated by Django 3.2.6 on 2024-03-29 22:11

import apps.accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_accountvalue_value_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountvalue',
            name='value_date',
            field=models.DateField(default=apps.accounts.models.return_date_time),
        ),
    ]
