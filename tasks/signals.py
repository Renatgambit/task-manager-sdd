from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Task


@receiver([post_save, post_delete], sender=Task)
def invalidate_dashboard_cache(**kwargs):
    cache.delete("taskflow:dashboard:v1")
