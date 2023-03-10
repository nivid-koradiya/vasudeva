# Generated by Django 4.1.7 on 2023-03-09 16:39

import databases.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("databases", "0016_quota_mail"),
    ]

    operations = [
        migrations.CreateModel(
            name="RechargeRate",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=databases.models.generate_uuid,
                        max_length=42,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("request_rate", models.IntegerField()),
                ("mail_rate", models.IntegerField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Recharge Rate",
                "verbose_name_plural": "Recharge Rates",
                "db_table": "recharge_rate",
            },
        ),
    ]
