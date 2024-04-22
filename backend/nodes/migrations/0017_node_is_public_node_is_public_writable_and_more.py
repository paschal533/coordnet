# Generated by Django 4.2.7 on 2024-04-16 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nodes", "0016_alter_space_deleted_nodes"),
    ]

    operations = [
        migrations.AddField(
            model_name="node",
            name="is_public",
            field=models.BooleanField(
                default=False, verbose_name="Whether the object is publicly available."
            ),
        ),
        migrations.AddField(
            model_name="node",
            name="is_public_writable",
            field=models.BooleanField(
                default=False,
                verbose_name="If the object is public, whether it is writable by unauthenticated users.",
            ),
        ),
        migrations.AddField(
            model_name="space",
            name="is_public",
            field=models.BooleanField(
                default=False, verbose_name="Whether the object is publicly available."
            ),
        ),
        migrations.AddField(
            model_name="space",
            name="is_public_writable",
            field=models.BooleanField(
                default=False,
                verbose_name="If the object is public, whether it is writable by unauthenticated users.",
            ),
        ),
    ]
