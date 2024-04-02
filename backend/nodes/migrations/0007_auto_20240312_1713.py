# Generated by Django 4.2.7 on 2024-03-12 17:13

from django.db import migrations
from django_celery_beat.models import PeriodicTask, IntervalSchedule


def create_periodic_task(apps, schema_editor):
    # Create a schedule that runs every 30 seconds
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=30, period=IntervalSchedule.SECONDS
    )

    # Create a periodic task that uses this schedule
    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name="Check trigger events every 30 seconds",
        task="nodes.tasks.check_trigger_events",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("nodes", "0006_space_title_slug_alter_space_deleted_nodes_and_more"),
    ]

    operations = [
        migrations.RunPython(
            create_periodic_task, reverse_code=migrations.RunPython.noop
        )
    ]