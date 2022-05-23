from django.urls import path

from . import views

app_name = "collector"
urlpatterns = [
    path("", views.ListPlacesView.as_view(), name="list_places"),
    path("add/", views.AddPlaceView.as_view(), name="add_place"),
]
