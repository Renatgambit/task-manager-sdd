from django.core.cache import cache
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TaskForm
from .models import Task


def task_list(request):
    stats = cache.get("taskflow:dashboard:v1")
    if stats is None:
        stats = Task.objects.aggregate(
            total=Count("id"),
            active=Count("id", filter=~Q(status=Task.Status.DONE)),
            done=Count("id", filter=Q(status=Task.Status.DONE)),
        )
        cache.set("taskflow:dashboard:v1", stats, timeout=60)

    tasks = Task.objects.all()
    status = request.GET.get("status", "")
    query = request.GET.get("q", "").strip()
    if status in Task.Status.values:
        tasks = tasks.filter(status=status)
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(
        request,
        "tasks/task_list.html",
        {"tasks": tasks, "stats": stats, "selected_status": status, "query": query, "statuses": Task.Status.choices},
    )


def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        task = form.save()
        return redirect("task_detail", pk=task.pk)
    return render(request, "tasks/task_form.html", {"form": form, "heading": "Новая задача"})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/task_detail.html", {"task": task})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("task_detail", pk=task.pk)
    return render(request, "tasks/task_form.html", {"form": form, "heading": "Редактировать задачу", "task": task})


@require_POST
def task_advance(request, pk):
    task = get_object_or_404(Task, pk=pk)
    order = [Task.Status.TODO, Task.Status.IN_PROGRESS, Task.Status.DONE]
    task.status = order[(order.index(task.status) + 1) % len(order)]
    task.save(update_fields=["status", "updated_at"])
    if request.POST.get("next") == "task_list":
        return redirect("task_list")
    return redirect("task_detail", pk=task.pk)


@require_POST
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect("task_list")
