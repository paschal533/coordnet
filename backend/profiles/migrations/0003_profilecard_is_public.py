# Generated by Django 5.1.3 on 2024-11-26 15:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0002_profilecard_created_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="profilecard",
            name="draft",
            field=models.BooleanField(default=False),
        ),
    ]
