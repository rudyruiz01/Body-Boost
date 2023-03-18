from django.urls import path
from . import views

app_name = "calculate"
urlpatterns = [
    path("", views.index, name="index"),
    path("meals", views.meals, name="meals")
]
