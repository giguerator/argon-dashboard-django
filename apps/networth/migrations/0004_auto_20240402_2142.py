# Generated by Django 3.2.6 on 2024-04-03 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core_assets', '0002_auto_20240402_2142'),
        ('networth', '0003_manualassetvalue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manualasset',
            name='current_value',
        ),
        migrations.RemoveField(
            model_name='manualasset',
            name='description',
        ),
        migrations.RemoveField(
            model_name='manualasset',
            name='id',
        ),
        migrations.RemoveField(
            model_name='manualasset',
            name='last_updated',
        ),
        migrations.RemoveField(
            model_name='manualasset',
            name='user',
        ),
        migrations.AddField(
            model_name='manualasset',
            name='asset_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core_assets.asset'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ManualAssetValue',
        ),
    ]
