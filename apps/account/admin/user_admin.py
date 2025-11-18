from django.contrib import admin
from apps.account.models.user_model import RBACPermission, Role, User


# <<------------------------------------*** RBAC Permission Admin ***------------------------------------>>
@admin.register(RBACPermission)
class RBACPermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active", "created_at", "updated_at")
    search_fields = ("name", "code")
    list_filter = ("is_active",)
    ordering = ("-id",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 10


# <<------------------------------------*** Role Admin ***------------------------------------>>
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_by", "is_active", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("is_active",)
    ordering = ("-id",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 10


# <<------------------------------------*** User Admin ***------------------------------------>>
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active", "is_staff", "is_deleted", "created_at", "updated_at")
    search_fields = ("username", "email")
    list_filter = ("is_active", "is_staff", "is_deleted")
    ordering = ("-id",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 10
