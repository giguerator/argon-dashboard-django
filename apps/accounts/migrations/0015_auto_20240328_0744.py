# Generated by Django 3.2.6 on 2024-03-28 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_account_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='institution',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
