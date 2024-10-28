from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "created_at",
    )
    list_display_links = ("username",)
    search_fields = ("username",)
    readonly_fields = ("created_at", "updated_at")


admin.site.empty_value_display = _("Empty")
