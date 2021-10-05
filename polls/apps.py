"""App polls."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Data and name."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
