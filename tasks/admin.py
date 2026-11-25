from django.contrib import admin

from .models import StudyCard


@admin.register(StudyCard)
class StudyCardAdmin(admin.ModelAdmin):
    list_display = ("question", "subject", "topic", "status", "difficulty", "next_review")
    list_filter = ("subject", "status", "difficulty")
    search_fields = ("question", "answer", "subject", "topic")
