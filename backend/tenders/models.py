from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import CreatedAtAndUpdatedAtMixin, UUIDFieldMixin
from organizations.models import Organization
from tenders.constants import (
    BID_NAME_LEN,
    SERVICE_TYPE_NAME_LEN,
    TENDER_NAME_LEN,
    VERSION_MIN_VALUE,
)
from users.models import User


class TenderStatus(models.TextChoices):
    CREATED = ("CREATED", _("Created"))
    PUBLISHED = ("PUBLISHED", _("Published"))
    CLOSED = ("CLOSED", _("Closed"))


class BidStatus(models.TextChoices):
    CREATED = ("CREATED", _("Created"))
    PUBLISHED = ("PUBLISHED", _("Published"))
    CLOSED = ("CANCELED", _("Canceled"))


class ServiceType(CreatedAtAndUpdatedAtMixin):
    name = models.CharField(
        _("Name"),
        max_length=SERVICE_TYPE_NAME_LEN,
        unique=True,
    )
    description = models.TextField(
        _("Description"),
    )

    class Meta:
        verbose_name = "Type of service"
        verbose_name_plural = "Types of services"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return str(self.name)


class TenderBase(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=TENDER_NAME_LEN,
    )
    description = models.TextField(
        _("Description"),
    )
    status = models.CharField(
        _("Status"),
        choices=TenderStatus.choices,
        unique=True,
        default="CREATED",
    )
    version = models.PositiveSmallIntegerField(
        _("Version"),
        default=VERSION_MIN_VALUE,
        validators=[
            MinValueValidator(
                VERSION_MIN_VALUE,
                message=_(f"Minimum version value {VERSION_MIN_VALUE}"),
            )
        ],
    )

    class Meta:
        abstract = True


class Tender(TenderBase, CreatedAtAndUpdatedAtMixin, UUIDFieldMixin):
    organization = models.ForeignKey(
        Organization,
        related_name="tenders",
        on_delete=models.CASCADE,
        verbose_name=_("Organization"),
    )
    creator = models.ForeignKey(
        User,
        related_name="tenders",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    service_type = models.ForeignKey(
        ServiceType,
        related_name="tenders",
        on_delete=models.CASCADE,
        verbose_name=_("Service type"),
    )

    class Meta:
        verbose_name = _("Tender")
        verbose_name_plural = _("Tenders")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return str(self.name)


class TenderHistory(TenderBase):
    tender = models.ForeignKey(
        Tender,
        related_name="history",
        on_delete=models.CASCADE,
        verbose_name=_("Tender"),
    )
    service_type = models.ForeignKey(
        ServiceType,
        related_name="history_tenders",
        on_delete=models.CASCADE,
        verbose_name=_("Service type"),
    )
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("Tender History")
        verbose_name_plural = _("Tender Histories")
        ordering = ("tender", "-version")
        unique_together = ("tender", "version")

    def __str__(self) -> str:
        return f"{self.tender.name} -> version {self.version}"


class BidBase(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=BID_NAME_LEN,
    )
    description = models.TextField(
        _("Description"),
    )
    status = models.CharField(
        _("Status"),
        choices=BidStatus.choices,
        unique=True,
        default="CREATED",
    )
    version = models.PositiveSmallIntegerField(
        _("Version"),
        default=VERSION_MIN_VALUE,
        validators=[
            MinValueValidator(
                VERSION_MIN_VALUE,
                message=_(f"Minimum version value {VERSION_MIN_VALUE}"),
            )
        ],
    )

    class Meta:
        abstract = True


class Bid(BidBase, CreatedAtAndUpdatedAtMixin, UUIDFieldMixin):
    organization = models.ForeignKey(
        Organization,
        related_name="bids",
        on_delete=models.CASCADE,
        verbose_name=_("Organization"),
    )
    creator = models.ForeignKey(
        User,
        related_name="bids",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    tender = models.ForeignKey(
        Tender,
        related_name="bids",
        on_delete=models.CASCADE,
        verbose_name=_("Tender"),
        null=True,
    )

    class Meta:
        verbose_name = _("Bid")
        verbose_name_plural = _("Bids")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return str(self.name)


class BidHistory(BidBase):
    bid = models.ForeignKey(
        Bid,
        related_name="history",
        on_delete=models.CASCADE,
        verbose_name=_("Bid"),
    )
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("Bid history")
        verbose_name_plural = _("Bid history")
        ordering = ("-created_at",)
        unique_together = ("bid", "version")

    def __str__(self) -> str:
        return f"{self.bid.name} -> version {self.version}"
