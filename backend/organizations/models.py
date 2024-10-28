from django.db import models
from django.utils.translation import gettext_lazy as _

from core.mixins import CreatedAtAndUpdatedAtMixin, UUIDFieldMixin
from organizations.constants import NULL_BLANK, ORGANIZATION_NAME_LEN
from users.models import User


class OrganizationType(models.TextChoices):
    IE = ("IE", _("Individual Entrepreneur"))
    LLC = ("LLC", _("Limited Liability Company"))
    JSC = ("JSC", _("Join-Stock Company"))


class OrganizationResponsible(UUIDFieldMixin):
    organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        verbose_name=_("Organization"),
    )
    user = models.ForeignKey(
        User,
        related_name="responsible_organizations",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )

    class Meta:
        verbose_name = _("Organization responsible")
        verbose_name_plural = _("Organizations responsible")

    def __str__(self) -> str:
        return f"{self.user} -> {self.organization.name}"


class Organization(CreatedAtAndUpdatedAtMixin, UUIDFieldMixin):
    name = models.CharField(
        _("Organization name"),
        unique=True,
        max_length=ORGANIZATION_NAME_LEN,
    )
    description = models.TextField(
        _("Description"),
        **NULL_BLANK,
    )
    type = models.CharField(
        _("Organization type"),
        choices=OrganizationType.choices,
        unique=True,
    )

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ("-created_at",)

    def is_responsible(self, user: User) -> bool:
        """Checks whether the given user is responsible for the organization.
        :param user: User object.
        """
        return OrganizationResponsible.objects.filter(
            organization=self,
            user=user,
        ).exists()

    def __str__(self) -> str:
        return str(self.name)
