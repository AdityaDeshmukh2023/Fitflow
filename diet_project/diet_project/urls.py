# diet_project/urls.py
from django.contrib import admin
from django.urls import path
from diet_recommendation import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.diet_recommendation_view, name="diet_recommendation"),
]
