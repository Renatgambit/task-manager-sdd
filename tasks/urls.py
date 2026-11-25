from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("tasks/new/", views.task_create, name="task_create"),
    path("tasks/<int:pk>/", views.task_detail, name="task_detail"),
    path("tasks/<int:pk>/edit/", views.task_update, name="task_update"),
    path("tasks/<int:pk>/advance/", views.task_advance, name="task_advance"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),
]
