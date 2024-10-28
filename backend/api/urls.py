from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.apps import ApiConfig
from api.views import PingView
from api.viewsets import BidViewSet, TenderViewSet

app_name = ApiConfig.name
router_v1 = DefaultRouter()

router_v1.register("tenders", TenderViewSet, basename="tenders")
router_v1.register("bids", BidViewSet, basename="bids")

urlpatterns = [
    path("", include(router_v1.urls)),
    path("ping/", PingView.as_view()),
]
