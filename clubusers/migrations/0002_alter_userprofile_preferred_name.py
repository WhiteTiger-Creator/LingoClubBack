# Generated by Django 4.2.9 on 2024-03-18 19:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clubusers", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="preferred_name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
