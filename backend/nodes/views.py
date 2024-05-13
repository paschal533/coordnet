import typing

import django.contrib.postgres.search as pg_search
import dry_rest_permissions.generics as dry_permissions
from django import http
from django.db import models as django_models
from rest_framework import decorators, generics, pagination, response

import permissions.managers
import permissions.models
import permissions.views
from nodes import filters, models, serializers
from utils import filters as base_filters
from utils import views

if typing.TYPE_CHECKING:
    from rest_framework import request


class NodeModelViewSet(
    permissions.views.PermissionViewSetMixin[models.Node],
    views.BaseReadOnlyModelViewSet[models.Node],
):
    """API endpoint that allows nodes to be viewed."""

    serializer_class = serializers.NodeSerializer
    filterset_fields = ("spaces",)
    filter_backends = (filters.NodePermissionFilterBackend, base_filters.BaseFilterBackend)
    permission_classes = (dry_permissions.DRYObjectPermissions,)

    def get_queryset(
        self,
    ) -> "permissions.managers.SoftDeletableMembershipModelQuerySet[models.Node]":
        queryset = models.Node.available_objects.prefetch_related(
            django_models.Prefetch(
                "subnodes",
                to_attr="available_subnodes",
                queryset=models.Node.available_objects.only("id", "public_id"),
            )
        )
        assert isinstance(queryset, permissions.managers.SoftDeletableMembershipModelQuerySet)
        return queryset.annotate_user_permissions(request=self.request)


class SpaceModelViewSet(
    permissions.views.PermissionViewSetMixin[models.Space], views.BaseModelViewSet[models.Space]
):
    """API endpoint that allows projects to be viewed or edited."""

    queryset = models.Space.available_objects.prefetch_related("nodes").all()
    serializer_class = serializers.SpaceSerializer
    filter_backends = (filters.SpacePermissionFilterBackend, base_filters.BaseFilterBackend)
    permission_classes = (dry_permissions.DRYObjectPermissions,)

    def get_queryset(
        self,
    ) -> "permissions.managers.SoftDeletableMembershipModelQuerySet[models.Space]":
        queryset = models.Space.available_objects.annotate(
            node_count=django_models.Count("nodes", filter=~django_models.Q(nodes__is_removed=True))
        )
        assert isinstance(queryset, permissions.managers.SoftDeletableMembershipModelQuerySet)
        return queryset.annotate_user_permissions(request=self.request)


class DocumentVersionModelViewSet(views.BaseReadOnlyModelViewSet[models.DocumentVersion]):
    """API endpoint that allows document versions to be viewed."""

    queryset = models.DocumentVersion.available_objects.all()
    serializer_class = serializers.DocumentVersionSerializer
    filterset_class = filters.DocumentVersionFilterSet
    filter_backends = (
        filters.DocumentVersionPermissionFilterBackend,
        base_filters.BaseFilterBackend,
    )
    permission_classes = (dry_permissions.DRYObjectPermissions,)
    pagination_class = pagination.PageNumberPagination

    @decorators.action(detail=True, methods=["get"])
    def crdt(self, request: "request.Request", public_id: str | None = None) -> http.HttpResponse:
        document_version = self.get_object()
        return http.HttpResponse(document_version.data, content_type="application/octet-stream")


class SearchView(generics.ListAPIView):
    """API endpoint that allows searching for nodes."""

    queryset = models.Node.available_objects.none()

    def get(
        self, request: "request.Request", *args: typing.Any, **kwargs: typing.Any
    ) -> response.Response:
        search_query_serializer = serializers.NodeSearchQuerySerializer(
            data=request.query_params, context={"request": request}
        )
        search_query_serializer.is_valid(raise_exception=True)

        nodes = (
            models.Node.available_objects.filter(
                models.Node.get_user_has_permission_filter(permissions.models.READ, request.user)
            )
            .prefetch_related(
                django_models.Prefetch(
                    "spaces", queryset=models.Space.available_objects.only("id", "public_id")
                )
            )
            .annotate(
                rank=pg_search.SearchRank(
                    pg_search.SearchVector("title", "text", config="english"),
                    pg_search.SearchQuery(search_query_serializer.validated_data["q"]),
                ),
                search=pg_search.SearchVector("title", "text", config="english"),
            )
            .filter(search=pg_search.SearchQuery(search_query_serializer.validated_data["q"]))
            .order_by("-rank")
        )

        if "space" in search_query_serializer.validated_data:
            nodes = nodes.filter(spaces=search_query_serializer.validated_data["space"])

        page = self.paginate_queryset(nodes)
        if page is not None:
            serializer = serializers.NodeSearchResultSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = serializers.NodeSearchResultSerializer(
            nodes, many=True, context={"request": request}
        )
        return response.Response(serializer.data)
