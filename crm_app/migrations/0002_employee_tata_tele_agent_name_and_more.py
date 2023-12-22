# Generated by Django 4.2.5 on 2023-12-20 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='tata_tele_agent_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='tata_tele_api_key',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='tata_tele_authorization',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]