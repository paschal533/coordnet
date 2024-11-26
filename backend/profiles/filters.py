import typing

from django.db.models import Q
from dry_rest_permissions.generics import DRYPermissionFiltersBase

from permissions.models import ADMIN_ROLES

if typing.TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework import request, views

    import profiles.models


class ProfilePermissionFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(
        self, request: "request.Request", queryset: "QuerySet", view: "views.APIView"
    ) -> "QuerySet[not profiles.models.Profile]":
        """Only return profiles that the user has access to."""
        queryset_filters = Q(draft=False) & (Q(space__is_removed=False) | Q(space__isnull=True))
        if request.user and request.user.is_authenticated:
            queryset_filters |= Q(
                space__members__user=request.user,
                space__members__role__role__in=ADMIN_ROLES,
                space__is_removed=False,
            ) | Q(user=request.user)

        return queryset.filter(queryset_filters).distinct()


class ProfileCardPermissionFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(
        self, request: "request.Request", queryset: "QuerySet", view: "views.APIView"
    ) -> "QuerySet[profiles.models.ProfileCard]":
        """Only return profile cards that the user has access to."""
        queryset_filters = Q(profile__draft=False) & (
            Q(profile__space__is_removed=False) | Q(profile__space__isnull=True)
        )
        if request.user and request.user.is_authenticated:
            queryset_filters |= Q(
                profile__space__members__user=request.user,
                profile__space__members__role__role__in=ADMIN_ROLES,
                profile__space__is_removed=False,
            ) | Q(profile__user=request.user)
        return queryset.filter(queryset_filters).distinct()
