# Generated by Django 4.1.7 on 2023-03-02 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DataApp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_no",
            field=models.IntegerField(null=True, unique=True),
        ),
    ]