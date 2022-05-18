from django.urls import path
from place_collector.collector import views


app_name = "collector"
urlpatterns = [
    path("", views.ListPlacesView.as_view(), name="list_places"),
]
