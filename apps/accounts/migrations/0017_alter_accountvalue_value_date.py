# Generated by Django 3.2.6 on 2024-03-28 22:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20240328_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountvalue',
            name='value_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
