from pathlib import Path

from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Templates Directory
TEMPLATES_DIR = BASE_DIR / "templates"
# Static Directory
STATIC_DIR = BASE_DIR / "static"
# Media Directory
MEDIA_DIR = BASE_DIR / "media"


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-hp!26pg2*j24)z9+yvm0zuh*ocu8!xrx#t)+nz=jpyq#l+#l9r"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# <<------------------------------------*** Application Settings ***------------------------------------>>
THIRD_PARTY_APPS = ["django_filters", "widget_tweaks"]
CUSTOM_APPS = [
    "apps.account.apps.AccountConfig",
    "apps.common.apps.CommonConfig",
    "apps.authority.apps.AuthorityConfig",
    "apps.author.apps.AuthorConfig",
    "apps.home.apps.HomeConfig",
    "apps.book.apps.BookConfig",
    "apps.subscription.apps.SubscriptionConfig",
    "apps.order.apps.OrderConfig",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    *THIRD_PARTY_APPS,
    *CUSTOM_APPS,
]

# <<------------------------------------*** Middleware Settings ***------------------------------------>>
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# <<------------------------------------*** Templates Settings ***------------------------------------>>
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# <<------------------------------------*** Database Settings ***------------------------------------>>
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# <<------------------------------------*** Time Zone Settings ***------------------------------------>>

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_TZ = True

# <<------------------------------------*** Static Files Settings ***------------------------------------>>
STATIC_URL = "static/"
STATICFILES_DIRS = [STATIC_DIR]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "account.User"

# LOGIN_REDIRECT_URL = "/home/"
LOGIN_URL = "/login/"

# Media files(Uploaded Files)
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Messages Setting
MESSAGE_TAGS = {messages.ERROR: "danger"}

# <<------------------------------------*** SSL Commerz Settings ***------------------------------------>>
SSLCOMMERZ_STORE_ID = "trian62cc10ef4bb1f"
SSLCOMMERZ_STORE_PASS = "trian62cc10ef4bb1f@ssl"


# <<------------------------------------*** Logging Settings ***------------------------------------>>
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} [{module}:{lineno}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": "DEBUG",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.utils.autoreload": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
