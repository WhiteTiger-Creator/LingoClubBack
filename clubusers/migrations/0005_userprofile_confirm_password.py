# Generated by Django 4.2.9 on 2024-03-18 19:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clubusers", "0004_remove_userprofile_confirm_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="confirm_password",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]