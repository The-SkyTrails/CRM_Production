# Generated by Django 4.2.5 on 2023-12-20 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media/Employee/profile_pic/'),
        ),
    ]
