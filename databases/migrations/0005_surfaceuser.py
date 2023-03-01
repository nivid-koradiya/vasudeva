# Generated by Django 4.1.6 on 2023-02-09 14:19

import databases.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0004_loginlog_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurfaceUser',
            fields=[
                ('id', models.CharField(default=databases.models.generate_uuid, max_length=42, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('username', models.CharField(default='user', max_length=64)),
                ('password', models.CharField(default='', max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
                ('desc', models.CharField(max_length=10000)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databases.client')),
            ],
        ),
    ]