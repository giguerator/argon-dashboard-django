# Generated by Django 3.2.6 on 2024-03-28 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('networth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manualasset',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
