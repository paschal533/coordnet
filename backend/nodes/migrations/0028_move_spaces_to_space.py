# Generated by Django 5.1.3 on 2024-11-12 09:42

from django.db import migrations


def move_space_membership_to_node(apps, schema_editor):
    Node = apps.get_model("nodes", "Node")

    for node in Node.objects.only("id", "space_id"):
        if node.space_id is not None:
            continue

        before = node.space_id
        node.space = node.spaces.first()

        # update_fields is faster than a normal save, but we need to check if the space actually
        # changed, otherwise an error will be raised
        if before != node.space_id:
            node.save(update_fields=["space_id"])


def move_space_membership_to_spaces(apps, schema_editor):
    Node = apps.get_model("nodes", "Node")
    Space = apps.get_model("nodes", "Space")

    for node in Node.objects.only("id", "space_id"):
        if node.space_id is None:
            continue

        # This might be a bit slow. Let's hope we don't have to migrate back.
        try:
            Space.objects.get(id=node.space_id).nodes.add(node)
        except Space.DoesNotExist:
            pass


class Migration(migrations.Migration):
    """
    Note: This assumes that we currently don't have any nodes in multiple spaces, which is true if
    nodes weren't created manually. If there are nodes in multiple spaces, this migration will just
    move them to the first space they are in.
    """

    dependencies = [
        ("nodes", "0027_node_space_alter_space_default_node"),
    ]

    operations = [
        migrations.RunPython(move_space_membership_to_node),
        migrations.RunPython(move_space_membership_to_spaces),
    ]