# Generated by Django 4.2.5 on 2023-12-27 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0015_remove_enquiry_mailing_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='emergency_email',
            field=models.EmailField(blank=True, default=1, max_length=254),
            preserve_default=False,
        ),
    ]
