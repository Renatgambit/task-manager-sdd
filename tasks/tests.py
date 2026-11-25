from django.core.cache import cache
from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskFlowTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_task_defaults(self):
        task = Task.objects.create(title="Сдать отчёт")
        self.assertEqual(task.status, Task.Status.TODO)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

    def test_stylesheet_is_discoverable(self):
        self.assertIsNotNone(finders.find("css/app.css"))

    def test_dashboard_shows_task_and_cached_counts(self):
        Task.objects.create(title="Первая задача")
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Первая задача")
        self.assertEqual(response.context["stats"]["total"], 1)

    def test_create_task(self):
        response = self.client.post(reverse("task_create"), {"title": "Новая", "status": "todo", "priority": "high"})
        self.assertEqual(Task.objects.count(), 1)
        self.assertRedirects(response, reverse("task_detail", args=[Task.objects.first().pk]))

    def test_edit_task(self):
        task = Task.objects.create(title="Черновик")
        response = self.client.post(
            reverse("task_update", args=[task.pk]),
            {"title": "Готовый заголовок", "description": "Обновлено", "status": "in_progress", "priority": "high", "due_date": ""},
        )
        task.refresh_from_db()
        self.assertEqual(task.title, "Готовый заголовок")
        self.assertEqual(task.status, Task.Status.IN_PROGRESS)
        self.assertRedirects(response, reverse("task_detail", args=[task.pk]))

    def test_advance_task_status_and_invalidate_dashboard_cache(self):
        task = Task.objects.create(title="Проверка")
        cache.set("taskflow:dashboard:v1", {"total": 1, "active": 1, "done": 0})
        response = self.client.post(reverse("task_advance", args=[task.pk]))
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.IN_PROGRESS)
        self.assertIsNone(cache.get("taskflow:dashboard:v1"))
        self.assertRedirects(response, reverse("task_detail", args=[task.pk]))

    def test_search_and_status_filter(self):
        Task.objects.create(title="Купить молоко")
        Task.objects.create(title="Написать код", status=Task.Status.DONE)
        response = self.client.get(reverse("task_list"), {"q": "код", "status": "done"})
        self.assertContains(response, "Написать код")
        self.assertNotContains(response, "Купить молоко")

    def test_delete_requires_post(self):
        task = Task.objects.create(title="Удаляемая")
        response = self.client.post(reverse("task_delete", args=[task.pk]))
        self.assertRedirects(response, reverse("task_list"))
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
