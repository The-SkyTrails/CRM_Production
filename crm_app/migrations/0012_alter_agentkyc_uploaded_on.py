# Generated by Django 4.2.5 on 2023-12-23 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0011_alter_agentkyc_uploaded_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentkyc',
            name='uploaded_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]