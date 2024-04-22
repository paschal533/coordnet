import typing

from django import http
from rest_framework import decorators

from nodes import filters, models, serializers
from utils import views

if typing.TYPE_CHECKING:
    from rest_framework import request


class NodeModelViewSet(views.BaseReadOnlyModelViewSet):
    """
    API endpoint that allows nodes to be viewed or edited.
    """

    queryset = models.Node.available_objects.all()
    serializer_class = serializers.NodeSerializer
    filterset_fields = ("spaces",)


class SpaceModelViewSet(views.BaseModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """

    queryset = models.Space.available_objects.prefetch_related("nodes").all()
    serializer_class = serializers.SpaceSerializer


class DocumentVersionModelViewSet(views.BaseReadOnlyModelViewSet):
    """
    API endpoint that allows document versions to be viewed or edited.
    """

    queryset = models.DocumentVersion.objects.all()
    serializer_class = serializers.DocumentVersionSerializer
    filterset_fields = ("document", "document_type")
    filterset_class = filters.DocumentVersionFilterSet

    @decorators.action(detail=True, methods=["get"])
    def crdt(self, request: "request.Request", public_id: str | None = None) -> http.HttpResponse:
        document_version = self.get_object()
        return http.HttpResponse(document_version.data, content_type="application/octet-stream")
