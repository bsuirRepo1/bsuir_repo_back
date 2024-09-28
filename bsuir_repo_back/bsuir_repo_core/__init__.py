from .wsgi import application # noqa
from .asgi import application # noqa
from .celery import app as celery_app

__all__ = ('celery_app',)
