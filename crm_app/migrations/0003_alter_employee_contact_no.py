# Generated by Django 4.2.5 on 2023-12-20 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0002_alter_employee_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='contact_no',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
