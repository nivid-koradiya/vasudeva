# Generated by Django 4.1.6 on 2023-02-06 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0007_quota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quota',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='databases.quota'),
        ),
    ]
