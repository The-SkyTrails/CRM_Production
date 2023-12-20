# Generated by Django 4.2.5 on 2023-12-15 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0013_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='lastupdated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]