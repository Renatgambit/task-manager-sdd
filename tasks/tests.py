from datetime import timedelta

from django.contrib.staticfiles import finders
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import StudyCard


class ExamPrepTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_card_defaults(self):
        card = StudyCard.objects.create(question="Что такое SDD?", answer="Разработка от спецификации")
        self.assertEqual(card.subject, "Общий предмет")
        self.assertEqual(card.status, StudyCard.Status.NEW)
        self.assertEqual(card.difficulty, StudyCard.Difficulty.MEDIUM)

    def test_stylesheet_is_discoverable(self):
        self.assertIsNotNone(finders.find("css/app.css"))

    def test_dashboard_shows_card_and_cached_counts(self):
        StudyCard.objects.create(question="Первая карточка", answer="Ответ", subject="История")
        response = self.client.get(reverse("card_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Первая карточка")
        self.assertEqual(response.context["stats"]["total"], 1)
        self.assertEqual(response.context["stats"]["subjects"], 1)

    def test_create_card(self):
        response = self.client.post(
            reverse("card_create"),
            {"subject": "Биология", "topic": "Клетка", "question": "Что такое ДНК?", "answer": "Носитель наследственной информации", "status": "new", "difficulty": "high", "next_review": ""},
        )
        self.assertEqual(StudyCard.objects.count(), 1)
        self.assertRedirects(response, reverse("card_detail", args=[StudyCard.objects.first().pk]))

    def test_edit_card(self):
        card = StudyCard.objects.create(question="Черновик", answer="Ответ")
        response = self.client.post(
            reverse("card_update", args=[card.pk]),
            {"subject": "Математика", "topic": "Алгебра", "question": "Обновлённый вопрос", "answer": "Обновлённый ответ", "status": "review", "difficulty": "high", "next_review": ""},
        )
        card.refresh_from_db()
        self.assertEqual(card.question, "Обновлённый вопрос")
        self.assertEqual(card.status, StudyCard.Status.REVIEW)
        self.assertRedirects(response, reverse("card_detail", args=[card.pk]))

    def test_mark_known_invalidates_dashboard_cache(self):
        card = StudyCard.objects.create(question="Проверка", answer="Ответ")
        cache.set("examprep:dashboard:v1", {"total": 1, "new": 1, "known": 0})
        response = self.client.post(reverse("review_card", args=[card.pk]), {"action": "known"})
        card.refresh_from_db()
        self.assertEqual(card.status, StudyCard.Status.KNOWN)
        self.assertIsNone(cache.get("examprep:dashboard:v1"))
        self.assertRedirects(response, reverse("study_session"))

    def test_search_and_status_filter(self):
        StudyCard.objects.create(question="Клетка", answer="Биологический вопрос", subject="Биология")
        StudyCard.objects.create(question="Производная", answer="Алгебраический вопрос", subject="Математика", status=StudyCard.Status.KNOWN)
        response = self.client.get(reverse("card_list"), {"q": "производная", "status": "known", "subject": "Математика"})
        self.assertContains(response, "Производная")
        self.assertNotContains(response, "Клетка")

    def test_delete_requires_post(self):
        card = StudyCard.objects.create(question="Удаляемая карточка", answer="Ответ")
        response = self.client.post(reverse("card_delete", args=[card.pk]))
        self.assertRedirects(response, reverse("card_list"))
        self.assertFalse(StudyCard.objects.filter(pk=card.pk).exists())

    def test_study_hides_answer_until_requested(self):
        StudyCard.objects.create(question="Первый закон Ньютона?", answer="Закон инерции", subject="Физика")
        response = self.client.get(reverse("study_session"))
        self.assertContains(response, "Первый закон Ньютона?")
        self.assertNotContains(response, "Закон инерции")
        response = self.client.get(reverse("study_session"), {"card": StudyCard.objects.first().pk, "show": "1"})
        self.assertContains(response, "Закон инерции")

    def test_again_action_schedules_card_for_tomorrow(self):
        card = StudyCard.objects.create(question="Повторить", answer="Ответ", subject="Физика")
        response = self.client.post(reverse("review_card", args=[card.pk]), {"action": "again", "subject": "Физика"})
        card.refresh_from_db()
        self.assertEqual(card.status, StudyCard.Status.REVIEW)
        self.assertEqual(card.next_review, timezone.localdate() + timedelta(days=1))
        self.assertIn("skip", response.url)

    def test_future_review_card_is_not_due(self):
        StudyCard.objects.create(question="Не сегодня", answer="Ответ", status=StudyCard.Status.REVIEW, next_review=timezone.localdate() + timedelta(days=1))
        response = self.client.get(reverse("study_session"))
        self.assertIsNone(response.context["card"])
