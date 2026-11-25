from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160, verbose_name="Название")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                ("status", models.CharField(choices=[("todo", "К выполнению"), ("in_progress", "В работе"), ("done", "Готово")], default="todo", max_length=20, verbose_name="Статус")),
                ("priority", models.CharField(choices=[("low", "Низкий"), ("medium", "Средний"), ("high", "Высокий")], default="medium", max_length=10, verbose_name="Приоритет")),
                ("due_date", models.DateField(blank=True, null=True, verbose_name="Срок")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
            ],
            options={"verbose_name": "задача", "verbose_name_plural": "задачи", "ordering": ["status", "-created_at"]},
        ),
    ]
