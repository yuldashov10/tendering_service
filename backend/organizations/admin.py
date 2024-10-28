from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from organizations.models import Organization, OrganizationResponsible


@admin.register(OrganizationResponsible)
class OrganizationResponsibleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "organization",
        "user",
    )
    list_display_links = ("id",)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
        "created_at",
    )
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("type",)
    readonly_fields = ("created_at", "updated_at")


admin.site.empty_value_display = _("Empty")
