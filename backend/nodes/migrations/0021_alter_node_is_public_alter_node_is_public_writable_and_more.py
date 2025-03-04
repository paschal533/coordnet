# Generated by Django 5.0.4 on 2024-05-06 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nodes", "0020_node_editor_document_node_graph_document_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="node",
            name="is_public",
            field=models.BooleanField(default=False, verbose_name="Public read access"),
        ),
        migrations.AlterField(
            model_name="node",
            name="is_public_writable",
            field=models.BooleanField(
                default=False,
                verbose_name="Public write access, if public read access is enabled",
            ),
        ),
        migrations.AlterField(
            model_name="space",
            name="is_public",
            field=models.BooleanField(default=False, verbose_name="Public read access"),
        ),
        migrations.AlterField(
            model_name="space",
            name="is_public_writable",
            field=models.BooleanField(
                default=False,
                verbose_name="Public write access, if public read access is enabled",
            ),
        ),
    ]
