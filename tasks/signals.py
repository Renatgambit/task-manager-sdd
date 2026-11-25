from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import StudyCard


@receiver([post_save, post_delete], sender=StudyCard)
def invalidate_dashboard_cache(**kwargs):
    cache.delete("examprep:dashboard:v1")
