from django.forms import widgets
from django.utils.safestring import mark_safe
from string import Template


class CustomPictureImageFieldWidget(widgets.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        default_html = super().render(name, value, attrs, renderer)

        img_html = ""
        if value and hasattr(value, "url"):
            img_html = mark_safe(f'<img src="{value.url}" height="150" width="130" style="display:block; margin-bottom:10px;">')

        return mark_safe(f"{img_html}{default_html}")
