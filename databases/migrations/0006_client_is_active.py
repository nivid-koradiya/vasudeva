# Generated by Django 4.1.6 on 2023-02-05 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0005_client_mobile_clientadmin_client_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
