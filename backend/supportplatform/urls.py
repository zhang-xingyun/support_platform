from django.urls import path
from rest_framework import routers

from .views import (
    PublishedVersionViewSet,
    DownloadRecordViewSet,
    ReleaseTypeViewSet,
)

system_url = routers.SimpleRouter()
system_url.register(r"release_version", PublishedVersionViewSet)
system_url.register(r"download_record", DownloadRecordViewSet)
system_url.register(r"type", ReleaseTypeViewSet)


urlpatterns = [
    # path(
    #     "resource_lazy_tree/",
    #     PublishedVersionViewSet.as_view({"get": "resource_lazy_tree"}),
    # ),
    # path(
    #     "resource_sub_lazy_tree/",
    #     PublishedVersionViewSet.as_view({"get": "resource_sub_lazy_tree"}),
    # ),
]
urlpatterns += system_url.urls
