from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account.models.choices import GenderChoices
from apps.common.models import BaseModel


# <<------------------------------------*** RBAC Permission Manager ***------------------------------------>>
class RBACPermissionManager(models.Manager):
    def get_all_permissions(self):
        return self.all()

    def get_all_active_permissions(self):
        return self.filter(is_active=True)


# <<------------------------------------*** RBAC Permission Model ***------------------------------------>>
class RBACPermission(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=100, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    for_permission = models.CharField(max_length=100, null=True, blank=True)

    objects = RBACPermissionManager()

    class Meta:
        db_table = "rbac_permission"
        verbose_name = "RBAC Permission"
        verbose_name_plural = "RBAC Permissions"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<RBACPermission: {self.name}, {self.pk}>"


# <<------------------------------------*** Role Manager ***------------------------------------>>
class RoleManager(models.Manager):
    def get_all_role(self):
        return self.all()

    def get_all_active_role(self):
        return self.filter(is_active=True)


# <<------------------------------------*** Role Model ***------------------------------------>>
class Role(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="role_created_by")
    permissions = models.ManyToManyField(RBACPermission, blank=True, related_name="roles_permissions")
    is_active = models.BooleanField(default=True)

    objects = RoleManager()

    class Meta:
        db_table = "role"
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Role: {self.name}, {self.pk}>"


# <<------------------------------------*** User Manager ***------------------------------------>>
class UserManager(BaseUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        if not username or not email or not password:
            raise ValueError(_("You must provide valid username, email and password"))

        user = self.model(username=username, email=email, password=password, is_superuser=True, is_staff=True)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError(_("You must provide a username"))

        if not email:
            raise ValueError(_("You must provide a email"))

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save()
        return user


# <<------------------------------------*** User Model ***------------------------------------>>
class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=100, unique=True, null=True, blank=True, validators=[UnicodeUsernameValidator()])
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    role = models.ForeignKey(Role, blank=True, null=True, on_delete=models.SET_NULL, related_name="user_role")
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    contact_no = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GenderChoices.choices, default=GenderChoices.UNMENTIONED, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="user_documents/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_short_name(self):
        # Return first_name or username as fallback
        return self.first_name if self.first_name else self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.username}"

    def get_user_rbac_permissions(self):
        return self.role.permissions.all().prefetch_related("permissions")

    def has_rbac_permission(self, code: str) -> bool:
        """
        Check if user has a specific RBAC permission by its code.
        """
        if not self.role:
            return False

        return self.role.permissions.filter(code=code, is_active=True).exists()

    def __repr__(self):
        return f"<User: {self.username}, {self.pk}>"
