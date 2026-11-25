from django.urls import path

from . import views

urlpatterns = [
    path("", views.card_list, name="card_list"),
    path("cards/new/", views.card_create, name="card_create"),
    path("cards/<int:pk>/", views.card_detail, name="card_detail"),
    path("cards/<int:pk>/edit/", views.card_update, name="card_update"),
    path("cards/<int:pk>/delete/", views.card_delete, name="card_delete"),
    path("study/", views.study_session, name="study_session"),
    path("study/<int:pk>/review/", views.review_card, name="review_card"),
]
