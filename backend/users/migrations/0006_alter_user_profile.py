# Generated by Django 5.1.3 on 2024-11-25 19:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
        ("users", "0005_fill_profiles"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to="profiles.profile",
            ),
        ),
    ]