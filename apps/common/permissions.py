from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class StaffPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class RBACPermissionRequiredMixin:
    """
    Mixin to check if a user has a specific RBAC permission or is superuser.
    Usage: set `required_permission = "permission_code"` in the CBV
    """

    required_permission = None  # override in CBV

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if self.required_permission and not request.user.has_rbac_permission(self.required_permission):
            raise PermissionDenied("You do not have permission to access this page.")

        return super().dispatch(request, *args, **kwargs)
