# Generated by Django 3.2.6 on 2024-03-23 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_account_institution'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='parent_institution',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='accounts.institution'),
            preserve_default=False,
        ),
    ]
