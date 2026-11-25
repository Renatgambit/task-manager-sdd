from django.db import migrations, models


def translate_legacy_statuses(apps, schema_editor):
    StudyCard = apps.get_model("tasks", "StudyCard")
    StudyCard.objects.filter(status="todo").update(status="new")
    StudyCard.objects.filter(status="in_progress").update(status="review")
    StudyCard.objects.filter(status="done").update(status="known")


def restore_legacy_statuses(apps, schema_editor):
    StudyCard = apps.get_model("tasks", "StudyCard")
    StudyCard.objects.filter(status="new").update(status="todo")
    StudyCard.objects.filter(status="review").update(status="in_progress")
    StudyCard.objects.filter(status="known").update(status="done")


class Migration(migrations.Migration):
    dependencies = [("tasks", "0001_initial")]

    operations = [
        migrations.RenameModel(old_name="Task", new_name="StudyCard"),
        migrations.RenameField(model_name="studycard", old_name="title", new_name="question"),
        migrations.RenameField(model_name="studycard", old_name="description", new_name="answer"),
        migrations.RenameField(model_name="studycard", old_name="priority", new_name="difficulty"),
        migrations.RenameField(model_name="studycard", old_name="due_date", new_name="next_review"),
        migrations.AddField(
            model_name="studycard",
            name="subject",
            field=models.CharField(default="Общий предмет", max_length=120, verbose_name="Предмет"),
        ),
        migrations.AddField(
            model_name="studycard",
            name="topic",
            field=models.CharField(blank=True, default="", max_length=160, verbose_name="Тема"),
            preserve_default=False,
        ),
        migrations.RunPython(translate_legacy_statuses, restore_legacy_statuses),
        migrations.AlterField(
            model_name="studycard",
            name="question",
            field=models.CharField(max_length=240, verbose_name="Вопрос"),
        ),
        migrations.AlterField(
            model_name="studycard",
            name="answer",
            field=models.TextField(verbose_name="Ответ"),
        ),
        migrations.AlterField(
            model_name="studycard",
            name="status",
            field=models.CharField(
                choices=[("new", "Новый вопрос"), ("review", "Повторить"), ("known", "Знаю ответ")],
                default="new",
                max_length=20,
                verbose_name="Статус изучения",
            ),
        ),
        migrations.AlterField(
            model_name="studycard",
            name="difficulty",
            field=models.CharField(
                choices=[("low", "Лёгкий"), ("medium", "Средний"), ("high", "Сложный")],
                default="medium",
                max_length=10,
                verbose_name="Сложность",
            ),
        ),
        migrations.AlterField(
            model_name="studycard",
            name="next_review",
            field=models.DateField(blank=True, null=True, verbose_name="Повторить после"),
        ),
        migrations.AlterModelOptions(
            name="studycard",
            options={
                "ordering": ["subject", "topic", "-created_at"],
                "verbose_name": "экзаменационная карточка",
                "verbose_name_plural": "экзаменационные карточки",
            },
        ),
    ]
