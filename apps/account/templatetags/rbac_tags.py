from django import template

register = template.Library()


@register.filter
def has_permission(user, permission_code):
    """
    Usage in template:
    {% if request.user|has_permission:"can_view_user" %}
        ... show section ...
    {% endif %}
    Superusers can view everything automatically.
    """
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True  # superuser can view everything
    return user.has_rbac_permission(permission_code)
