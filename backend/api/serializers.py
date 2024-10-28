from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import (
    CharField,
    DateTimeField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    UUIDField,
)
from rest_framework.validators import ValidationError

from tenders.models import Bid, BidHistory, Organization, Tender, TenderHistory


class TenderSerializer(ModelSerializer):
    creatorUsername = CharField(source="creator.username", read_only=True)
    organizationId = UUIDField(source="organization.id", read_only=True)
    organization = PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        write_only=True,
    )
    serviceType = CharField(source="service_type")
    createdAt = DateTimeField(source="created_at", read_only=True)
    updatedAt = DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Tender
        fields = (
            "id",
            "name",
            "description",
            "serviceType",
            "status",
            "version",
            "organizationId",
            "organization",
            "creatorUsername",
            "createdAt",
            "updatedAt",
        )

    def validate(self, attrs):
        user = self.context.get("request").user
        organization = attrs.get("organization")

        if not organization.is_responsible(user):
            raise ValidationError(
                _(f"{user} is not responsible for the organization")
            )

        version = self.context.get("version")
        if (
            self.instance
            and version is not None
            and int(version) >= self.instance.version
        ):
            raise ValidationError(
                _(f"Can't roll back to version {version}"),
            )

        return attrs

    def update(self, instance, validated_data):
        TenderHistory.objects.create(
            tender=instance,
            name=instance.name,
            description=instance.description,
            service_type=instance.service_type,
            status=instance.status,
            version=instance.version,
        )

        instance.version += 1
        return super().update(instance, validated_data)


class BidSerializer(ModelSerializer):
    creatorUsername = CharField(source="creator.username", read_only=True)
    organizationId = UUIDField(source="organization.id", write_only=True)
    tenderId = UUIDField(source="tender.id", write_only=True)

    class Meta:
        model = Bid
        fields = (
            "id",
            "name",
            "description",
            "status",
            "tenderId",
            "organizationId",
            "creatorUsername",
        )

    def create(self, validated_data):
        organization_id = validated_data.pop("organization").get("id")
        tender_id = validated_data.pop("tender").get("id")
        organization = get_object_or_404(Organization, id=organization_id)
        tender = get_object_or_404(Tender, id=tender_id)

        return Bid.objects.create(
            organization=organization, tender=tender, **validated_data
        )

    def validate(self, attrs):
        version = self.context.get("version")
        if (
            self.instance
            and version is not None
            and int(version) >= self.instance.version
        ):
            raise ValidationError(
                _(f"Can't roll back to version {version}"),
            )
        return attrs

    def update(self, instance, validated_data):
        BidHistory.objects.create(
            bid=instance,
            name=instance.name,
            description=instance.description,
            status=instance.status,
            version=instance.version,
        )

        instance.version += 1
        return super().update(instance, validated_data)
