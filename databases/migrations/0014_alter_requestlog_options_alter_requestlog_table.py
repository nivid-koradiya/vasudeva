# Generated by Django 4.1.7 on 2023-03-08 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("databases", "0013_requestlog_method_requestlog_path"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="requestlog",
            options={
                "verbose_name": "Request Log",
                "verbose_name_plural": "Request Logs",
            },
        ),
        migrations.AlterModelTable(name="requestlog", table="request_log",),
    ]
