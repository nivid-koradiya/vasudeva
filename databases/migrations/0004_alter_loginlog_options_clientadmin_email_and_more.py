# Generated by Django 4.1.6 on 2023-02-05 14:30

import databases.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0003_client_clientadmin_alter_loginlog_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loginlog',
            options={'verbose_name': 'login_log', 'verbose_name_plural': 'login_logs'},
        ),
        migrations.AddField(
            model_name='clientadmin',
            name='email',
            field=models.EmailField(default='defaultmail@mail.com', max_length=254),
        ),
        migrations.AddField(
            model_name='clientadmin',
            name='name',
            field=models.CharField(default='default', max_length=125),
        ),
        migrations.AddField(
            model_name='clientadmin',
            name='password',
            field=models.CharField(default=databases.models.generate_default_password_hash, max_length=1280),
        ),
        migrations.AddField(
            model_name='clientadmin',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 2, 5, 14, 30, 15, 66880, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clientadmin',
            name='username',
            field=models.CharField(default='rocky1234', max_length=64, validators=[databases.models.validate_username]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='id',
            field=models.CharField(default=databases.models.generate_uuid, max_length=42, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='clientadmin',
            name='id',
            field=models.CharField(default=databases.models.generate_uuid, max_length=42, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='loginlog',
            name='id',
            field=models.CharField(default=databases.models.generate_uuid, max_length=42, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='loginlog',
            name='mode_of_login',
            field=models.CharField(choices=[('browser', 'browser'), ('other', 'other')], default='browser', max_length=100),
        ),
    ]
