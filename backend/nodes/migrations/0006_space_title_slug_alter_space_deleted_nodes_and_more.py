# Generated by Django 4.2.7 on 2024-03-12 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nodes", "0005_rename_project_space_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="space",
            name="title_slug",
            field=models.SlugField(default="", max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="space",
            name="deleted_nodes",
            field=models.ManyToManyField(
                related_name="spaces_deleted", to="nodes.node"
            ),
        ),
        migrations.AlterField(
            model_name="space",
            name="nodes",
            field=models.ManyToManyField(related_name="spaces", to="nodes.node"),
        ),
    ]