from rest_framework.permissions import SAFE_METHODS, BasePermission


class HasRole(BasePermission):
    allowed_roles = ()

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_superuser or request.user.role in self.allowed_roles)
        )


class IsAdministrator(HasRole):
    allowed_roles = ("administrator",)


class IsAdministratorOrManager(HasRole):
    allowed_roles = ("administrator", "manager")


class IsFarmStaff(HasRole):
    allowed_roles = ("administrator", "manager", "worker")


class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser or request.user.role in ("administrator", "manager"):
            return True
        return request.method in SAFE_METHODS and request.user.role == "worker"


class CanManageDailyRecords(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ("administrator", "manager", "worker")
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_superuser
            or request.user.role in ("administrator", "manager")
            or obj.created_by_id == request.user.id
        )
