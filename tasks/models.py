from django.db import models


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "К выполнению"
        IN_PROGRESS = "in_progress", "В работе"
        DONE = "done", "Готово"

    class Priority(models.TextChoices):
        LOW = "low", "Низкий"
        MEDIUM = "medium", "Средний"
        HIGH = "high", "Высокий"

    title = models.CharField("Название", max_length=160)
    description = models.TextField("Описание", blank=True)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.TODO)
    priority = models.CharField("Приоритет", max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    due_date = models.DateField("Срок", blank=True, null=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["status", "-created_at"]
        verbose_name = "задача"
        verbose_name_plural = "задачи"

    def __str__(self):
        return self.title
