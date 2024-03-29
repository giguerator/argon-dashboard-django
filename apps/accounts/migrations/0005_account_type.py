# Generated by Django 3.2.6 on 2024-03-21 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_account_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='type',
            field=models.CharField(choices=[('CR', 'Credit'), ('DB', 'Debit')], default='DB', max_length=2),
        ),
    ]