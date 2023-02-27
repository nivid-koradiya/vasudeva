# Generated by Django 4.1.6 on 2023-02-24 07:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("databases", "0008_apikeys_client"),
    ]

    operations = [
        migrations.AddField(
            model_name="apikeys",
            name="timestamp",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
