import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.constants import (
    FIRST_NAME_LEN,
    LAST_NAME_LEN,
    NULL_BLANK,
    USERNAME_LEN,
)


class User(AbstractUser):
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    id = models.UUIDField(
        _("Unique identifier"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    username = models.CharField(
        _("Username"),
        max_length=USERNAME_LEN,
        unique=True,
        validators=[UnicodeUsernameValidator()],
    )
    first_name = models.CharField(
        _("First name"),
        max_length=FIRST_NAME_LEN,
        **NULL_BLANK,
    )
    last_name = models.CharField(
        _("Last name"),
        max_length=LAST_NAME_LEN,
        **NULL_BLANK,
    )

    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return str(self.username)
