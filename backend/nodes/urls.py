from django.urls import path

from nodes import views
from utils import routers

app_name = "nodes"

router = routers.get_router()

router.register("nodes/nodes", views.NodeModelViewSet, basename="nodes")
router.register("nodes/methods", views.MethodNodeModelViewSet, basename="methods")
router.register("nodes/spaces", views.SpaceModelViewSet, basename="spaces")
router.register("nodes/versions", views.DocumentVersionModelViewSet, basename="document-versions")
router.register("nodes/method-runs", views.MethodNodeRunModelViewSet, basename="method-runs")
router.register(
    "nodes/method-versions", views.MethodNodeVersionModelViewSet, basename="method-versions"
)


urlpatterns = router.urls

urlpatterns += [
    path("nodes/search/", views.SearchView.as_view(), name="search"),
]
