# diet_project/diet_recommendation/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.diet_recommendation_view, name="diet_recommendation"),
    path(
        "history/",
        views.RecommendationHistoryView.as_view(),
        name="recommendation_history",
    ),
]
