from django.contrib import admin

from nodes import models
from permissions.admin import ObjectMembershipInline


@admin.register(models.Space)
class SpaceAdmin(admin.ModelAdmin):
    """
    Admin interface for the Space model.
    Includes ObjectMembershipInline for managing memberships directly from the Space admin page.
    """

    inlines = [ObjectMembershipInline]


admin.site.register(models.Document)
admin.site.register(models.DocumentEvent)
admin.site.register(models.DocumentVersion)
admin.site.register(models.Node)
admin.site.register(models.MethodNode)
admin.site.register(models.MethodNodeRun)
admin.site.register(models.MethodNodeVersion)
