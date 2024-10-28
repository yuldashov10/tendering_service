from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsResponsible(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.method in ("PATCH", "PUT")
            and obj.organization.is_responsible(request.user)
        )
