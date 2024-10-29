# Generated by Django 5.0.7 on 2024-10-29 15:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nodes", "0025_remove_document_document_change_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="space",
            name="default_node",
            field=models.ForeignKey(
                blank=True,
                help_text="The node that gets displayed when a space is opened.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="nodes.node",
            ),
        ),
        migrations.AlterField(
            model_name="space",
            name="nodes",
            field=models.ManyToManyField(
                blank=True, related_name="spaces", to="nodes.node"
            ),
        ),
    ]
