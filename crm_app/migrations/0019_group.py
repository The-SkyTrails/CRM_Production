# Generated by Django 4.2.5 on 2023-12-16 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0018_branch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100, unique=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('group_member', models.ManyToManyField(related_name='groups_member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]