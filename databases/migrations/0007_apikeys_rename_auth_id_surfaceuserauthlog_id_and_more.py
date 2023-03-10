# Generated by Django 4.1.6 on 2023-02-09 14:38

import databases.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0006_surfaceuserauthlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKeys',
            fields=[
                ('id', models.CharField(default=databases.models.generate_uuid, max_length=42, primary_key=True, serialize=False)),
                ('key_value', models.CharField(default=databases.models.generate_api_key, max_length=64)),
            ],
        ),
        migrations.RenameField(
            model_name='surfaceuserauthlog',
            old_name='auth_id',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='surfaceuserauthlog',
            name='valid_till',
        ),
    ]
