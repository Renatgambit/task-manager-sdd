from datetime import timedelta

from django.db import models
from django.utils import timezone


class StudyCard(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новый вопрос"
        REVIEW = "review", "Повторить"
        KNOWN = "known", "Знаю ответ"

    class Difficulty(models.TextChoices):
        LOW = "low", "Лёгкий"
        MEDIUM = "medium", "Средний"
        HIGH = "high", "Сложный"

    subject = models.CharField("Предмет", max_length=120, default="Общий предмет")
    topic = models.CharField("Тема", max_length=160, blank=True)
    question = models.CharField("Вопрос", max_length=240)
    answer = models.TextField("Ответ")
    status = models.CharField("Статус изучения", max_length=20, choices=Status.choices, default=Status.NEW)
    difficulty = models.CharField("Сложность", max_length=10, choices=Difficulty.choices, default=Difficulty.MEDIUM)
    next_review = models.DateField("Повторить после", blank=True, null=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["subject", "topic", "-created_at"]
        verbose_name = "экзаменационная карточка"
        verbose_name_plural = "экзаменационные карточки"

    def __str__(self):
        return self.question

    def mark_known(self):
        self.status = self.Status.KNOWN
        self.next_review = None
        self.save(update_fields=["status", "next_review", "updated_at"])

    def schedule_for_review(self, days=1):
        self.status = self.Status.REVIEW
        self.next_review = timezone.localdate() + timedelta(days=days)
        self.save(update_fields=["status", "next_review", "updated_at"])
