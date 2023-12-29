# Generated by Django 4.2.5 on 2023-12-27 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0020_merge_20231227_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('follow_up_status', models.CharField(blank=True, choices=[('Inprocess', 'Inprocess'), ('Done', 'Done')], max_length=20, null=True)),
                ('priority', models.CharField(blank=True, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=20, null=True)),
                ('calendar', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('enquiry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.enquiry')),
            ],
        ),
    ]
