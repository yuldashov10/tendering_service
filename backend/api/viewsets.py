from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsResponsible
from api.serializers import BidSerializer, TenderSerializer
from tenders.models import Bid, BidHistory, Tender, TenderHistory
from users.models import User


class TenderViewSet(ModelViewSet):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = (
        IsAuthenticated,
        IsResponsible,
    )
    http_method_names = ["get", "post", "patch", "put"]

    def list(self, request, *args, **kwargs):
        service_type = request.query_params.get("serviceType")
        if service_type is not None:
            self.queryset = self.queryset.filter(service_type=service_type)
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=("POST",), url_path="new")
    def create_tender(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=("PATCH",),
        url_path=r"(?P<id>[0-9a-f-]{32,36})/edit",
    )
    def update_tender(self, request, *args, **kwargs):
        tender = self.get_object()
        serializer = self.get_serializer(
            tender,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=("PUT",),
        url_path=r"(?P<id>[0-9a-f-]{32,36})/rollback/(?P<version>\d+)",
    )
    def rollback(self, request, pk=None, version=None):
        tender = self.get_object()
        history = get_object_or_404(
            TenderHistory,
            tender=tender,
            version=int(version),
        )
        tender.name = history.name
        tender.description = history.description
        tender.service_type = history.service_type
        tender.status = history.status
        tender.version = history.version
        serializer = self.get_serializer(tender)
        tender.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=("GET",),
        url_path="my",
    )
    def my_tenders(self, request):
        username = request.query_params.get("username")
        if username:
            user = get_object_or_404(User, username=username.rstrip("/"))
        else:
            user = request.user
        serializer = self.get_serializer(
            Tender.objects.filter(creator=user),
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=("POST",),
        url_path="status",
    )
    def change_status(self, request, pk=None):
        tender = self.get_object()
        new_status = request.data.get("status")
        if not new_status:
            return Response(
                data={"error": "Status is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if tender.status == "CREATED" and new_status == "PUBLISHED":
            tender.status = "PUBLISHED"
        elif tender.status == "PUBLISHED" and new_status == "CLOSED":
            tender.status = "CLOSED"
        else:
            return Response(
                data={
                    "error": _(
                        "Can't change status from "
                        f"{tender.status} to {new_status}"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        tender.save()
        serializer = self.get_serializer(tender)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BidViewSet(ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = (
        IsAuthenticated,
        IsResponsible,
    )
    http_method_names = ["get", "post", "patch", "put"]

    @action(
        detail=False,
        methods=("GET",),
        url_path=r"(?P<tender_id>[0-9a-f-]{32,36})/list",
    )
    def list_bids_for_tender(self, request, tender_id=None):
        tender = get_object_or_404(Tender, id=tender_id)
        serializer = self.get_serializer(
            Bid.objects.filter(tender=tender),
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=("POST",),
        url_path="new",
    )
    def create_bid(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=("PATCH",),
        url_path=r"(?P<id>[0-9a-f-]{32,36})/edit",
    )
    def update_bid(self, request, pk=None):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["put"],
        url_path=r"(?P<id>[0-9a-f-]{32,36})/rollback/(?P<version>\d+)",
    )
    def rollback(self, request, pk=None, version=None):
        bid = self.get_object()
        bid_history = get_object_or_404(
            BidHistory,
            bid=bid,
            version=int(version),
        )

        bid.name = bid_history.name
        bid.description = bid_history.description
        bid.status = bid_history.status
        bid.version = bid_history.version
        bid.save()

        serializer = self.get_serializer(bid)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=("GET",), url_path="my")
    def my_bids(self, request):
        username = request.query_params.get("username")
        if username:
            user = get_object_or_404(User, username=username.rstrip("/"))
        else:
            user = request.user
        serializer = self.get_serializer(
            Bid.objects.filter(creator=user),
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=("POST",), url_path="submit_decision")
    def submit_decision(self, request, pk=None):
        bid = self.get_object()
        decision = request.data.get("decision")
        if decision not in ["accept", "reject"]:
            return Response(
                data={
                    "error": _(
                        "Invalid decision. Must be 'accept' or 'reject'"
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if decision == "accept":
            bid.status = "PUBLISHED"
        elif decision == "reject":
            bid.status = "CANCELED"

        bid.save()
        serializer = self.get_serializer(bid)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=("POST",), url_path="status")
    def change_status(self, request, pk=None):
        bid = self.get_object()
        new_status = request.data.get("status")
        if not new_status:
            return Response(
                data={"error": "Status is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if bid.status == "CREATED" and new_status == "PUBLISHED":
            bid.status = "PUBLISHED"
        elif bid.status == "PUBLISHED" and new_status == "CLOSED":
            bid.status = "CLOSED"
        else:
            return Response(
                data={
                    "error": _(
                        "Can't change status from "
                        f"{bid.status} to {new_status}"
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        bid.save()
        serializer = self.get_serializer(bid)
        return Response(serializer.data, status=status.HTTP_200_OK)
