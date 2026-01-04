import random

from apps.account.models.user_model import User


def unique_hex_username(prefix="author", length=5):
    hex_chars = "0123456789ABCDEF"
    while True:
        rand = "".join(random.choices(hex_chars, k=length))
        username = f"{prefix}_{rand}@"
        if not User.objects.filter(username=username).exists():
            return username
