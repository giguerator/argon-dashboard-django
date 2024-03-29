# Generated by Django 5.0.3 on 2024-03-18 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='descripion',
        ),
        migrations.AddField(
            model_name='account',
            name='description',
            field=models.CharField(default='tata', max_length=400),
            preserve_default=False,
        ),
    ]