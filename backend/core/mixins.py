import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class CreatedAtAndUpdatedAtMixin(models.Model):
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True,
    )

    class Meta:
        abstract = True


class UUIDFieldMixin(models.Model):
    id = models.UUIDField(
        _("Unique identifier"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True
