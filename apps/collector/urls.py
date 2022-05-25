from django.urls import path

from . import views

app_name = "collector"
urlpatterns = [
    path(
        "",
        views.ListPlacesView.as_view(),
        name="list-places",
    ),
    path(
        "add/",
        views.AddPlaceView.as_view(),
        name="add-place",
    ),
    path(
        "<int:pk>/",
        views.DetailPlaceView.as_view(),
        name="detail-place",
    ),
    path(
        "<int:pk>/delete/",
        views.DeletePlaceView.as_view(),
        name="del-place",
    ),
    path(
        "<int:pk>/update/",
        views.UpdatePlaceView.as_view(),
        name="update-place",
    ),
]
