# Generated by Django 3.2.6 on 2024-04-04 02:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core_assets', '0004_alter_asset_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to=settings.AUTH_USER_MODEL),
        ),
    ]
