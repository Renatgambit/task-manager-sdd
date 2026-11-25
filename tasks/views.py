from urllib.parse import urlencode

from django.core.cache import cache
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import StudyCardForm
from .models import StudyCard


def card_list(request):
    stats = cache.get("examprep:dashboard:v1")
    if stats is None:
        stats = StudyCard.objects.aggregate(
            total=Count("id"),
            new=Count("id", filter=Q(status=StudyCard.Status.NEW)),
            known=Count("id", filter=Q(status=StudyCard.Status.KNOWN)),
            subjects=Count("subject", distinct=True),
        )
        cache.set("examprep:dashboard:v1", stats, timeout=60)

    cards = StudyCard.objects.all()
    status = request.GET.get("status", "")
    subject = request.GET.get("subject", "").strip()
    query = request.GET.get("q", "").strip()
    if status in StudyCard.Status.values:
        cards = cards.filter(status=status)
    cards = list(cards)
    if subject:
        subject_key = subject.casefold()
        cards = [card for card in cards if card.subject.casefold() == subject_key]
    if query:
        query_key = query.casefold()
        cards = [
            card
            for card in cards
            if any(
                query_key in value.casefold()
                for value in (card.subject, card.topic, card.question, card.answer)
            )
        ]

    return render(
        request,
        "tasks/task_list.html",
        {
            "cards": cards,
            "stats": stats,
            "selected_status": status,
            "selected_subject": subject,
            "query": query,
            "subjects": StudyCard.objects.order_by("subject").values_list("subject", flat=True).distinct(),
            "statuses": StudyCard.Status.choices,
        },
    )


def card_create(request):
    form = StudyCardForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        card = form.save()
        return redirect("card_detail", pk=card.pk)
    return render(request, "tasks/task_form.html", {"form": form, "heading": "Новая карточка"})


def card_detail(request, pk):
    card = get_object_or_404(StudyCard, pk=pk)
    return render(request, "tasks/task_detail.html", {"card": card})


def card_update(request, pk):
    card = get_object_or_404(StudyCard, pk=pk)
    form = StudyCardForm(request.POST or None, instance=card)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("card_detail", pk=card.pk)
    return render(request, "tasks/task_form.html", {"form": form, "heading": "Редактировать карточку", "card": card})


@require_POST
def review_card(request, pk):
    card = get_object_or_404(StudyCard, pk=pk)
    action = request.POST.get("action")
    if action == "known":
        card.mark_known()
    elif action == "again":
        card.schedule_for_review()
    else:
        return redirect("study_session")
    subject = request.POST.get("subject", "").strip()
    params = {"subject": subject} if subject else {}
    if action == "again":
        params["skip"] = card.pk
    query = urlencode(params)
    return redirect(f"{reverse('study_session')}?{query}" if query else "study_session")


def study_session(request):
    subject = request.GET.get("subject", "").strip()
    due = Q(next_review__isnull=True) | Q(next_review__lte=timezone.localdate())
    cards = StudyCard.objects.filter(status__in=[StudyCard.Status.NEW, StudyCard.Status.REVIEW]).filter(due)
    if subject:
        cards = cards.filter(subject__iexact=subject)
    requested_card = request.GET.get("card", "")
    if requested_card.isdigit():
        card = cards.filter(pk=int(requested_card)).first()
    else:
        skip = request.GET.get("skip", "")
        if skip.isdigit():
            cards = cards.exclude(pk=int(skip))
        card = cards.order_by("updated_at", "pk").first()
    return render(
        request,
        "tasks/study_session.html",
        {"card": card, "show_answer": request.GET.get("show") == "1", "selected_subject": subject},
    )


@require_POST
def card_delete(request, pk):
    card = get_object_or_404(StudyCard, pk=pk)
    card.delete()
    return redirect("card_list")
