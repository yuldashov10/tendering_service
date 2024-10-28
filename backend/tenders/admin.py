from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from tenders.models import Bid, ServiceType, Tender, TenderHistory


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
    )
    list_display_links = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "service_type",
        "status",
        "version",
        "organization",
        "creator",
        "created_at",
    )
    list_display_links = ("id",)
    list_filter = (
        "status",
        "service_type",
        "organization",
        "creator",
    )
    search_fields = (
        "name",
        "organization",
        "creator",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "status",
        "organization",
        "creator",
        "created_at",
    )
    list_filter = (
        "status",
        "organization",
        "creator",
    )
    search_fields = (
        "name",
        "organization",
        "creator",
    )
    readonly_fields = ("created_at", "updated_at")


admin.site.register(TenderHistory)
admin.site.empty_value_display = _("Empty")
