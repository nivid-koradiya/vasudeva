# Generated by Django 4.1.6 on 2023-02-06 15:40

import databases.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.CharField(default=databases.models.generate_uuid, max_length=42, primary_key=True, serialize=False)),
                ('organisation', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
                'db_table': 'clients',
            },
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.CharField(default=databases.models.generate_uuid, max_length=42, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('mode_of_login', models.CharField(choices=[('browser', 'browser'), ('other', 'other')], default='browser', max_length=100)),
            ],
            options={
                'verbose_name': 'Login log',
                'verbose_name_plural': 'Login logs',
                'db_table': 'log_login',
            },
        ),
        migrations.CreateModel(
            name='Quota',
            fields=[
                ('id', models.CharField(default=databases.models.generate_uuid, max_length=42, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='databases.client')),
            ],
            options={
                'verbose_name': 'Quota',
                'verbose_name_plural': 'Quotas',
                'db_table': 'quotas',
            },
        ),
        migrations.CreateModel(
            name='ClientAdmin',
            fields=[
                ('id', models.CharField(default=databases.models.generate_uuid, max_length=42, primary_key=True, serialize=False)),
                ('name', models.CharField(default='default', max_length=125)),
                ('username', models.CharField(max_length=64, validators=[databases.models.validate_username])),
                ('email', models.EmailField(default='defaultmail@mail.com', max_length=254)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='databases.client')),
            ],
            options={
                'verbose_name': 'ClientAdmin',
                'verbose_name_plural': 'ClientAdmins',
                'db_table': 'client_admin',
            },
        ),
    ]
