from .base import *  # noqa

DATABASES = {
    "default": env.db("DATABASE_URL")  # noqa
}

ALLOWED_HOSTS = ["*"]
