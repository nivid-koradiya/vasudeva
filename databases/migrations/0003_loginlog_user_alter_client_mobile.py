# Generated by Django 4.1.6 on 2023-02-08 09:29

import databases.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('databases', '0002_clientadmin_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginlog',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='mobile',
            field=models.CharField(max_length=10, validators=[databases.models.client_mobile_validator]),
        ),
    ]
