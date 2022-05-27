from django.urls import reverse, reverse_lazy
from rest_framework import status

from apps.collector.factories import PlaceFactory
from apps.collector.models import Place
from apps.users.models import User


def test_create_place(
    auth_client,
    user: User,
) -> None:
    """Test place creation."""
    place = PlaceFactory.build(
        user=user,
    )
    auth_client.cookies["latitude"] = place.latitude
    auth_client.cookies["longitude"] = place.longitude
    response = auth_client.post(
        reverse_lazy("collector:add-place"),
        data={
            "name": place.name,
            "description": place.description,
        },
    )
    assert response.status_code == status.HTTP_302_FOUND
    assert Place.objects.filter(
        name=place.name,
        description=place.description,
        latitude=place.latitude,
        longitude=place.longitude,
    ).exists()


def test_owner_remove_place(
    auth_client,
    user: User,
) -> None:
    """Test remove place by owner."""
    place = PlaceFactory.create(
        user=user,
    )
    auth_client.post(
        reverse("collector:del-place", kwargs={"pk": place.pk}),
    )
    assert place not in Place.objects.all()


def test_not_owner_remove_place(
    auth_client,
) -> None:
    """Test remove place by another user."""
    place = PlaceFactory.create()
    response = auth_client.post(
        reverse("collector:del-place", kwargs={"pk": place.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_owner_update_place(
    user: User,
    auth_client,
) -> None:
    """Test update place by owner."""
    place = PlaceFactory.create(
        user=user,
    )
    new_name = "My place"
    auth_client.cookies["latitude"] = place.latitude
    auth_client.cookies["longitude"] = place.longitude
    response = auth_client.post(
        reverse_lazy("collector:update-place", kwargs={"pk": place.pk}),
        data={
            "name": new_name,
            "description": place.description,
        },
    )
    assert response.status_code == status.HTTP_302_FOUND
    assert Place.objects.filter(
        name=new_name,
        description=place.description,
        latitude=place.latitude,
        longitude=place.longitude,
    ).exists()


def test_not_owner_update_place(
    auth_client,
) -> None:
    """Test update place by another user."""
    place = PlaceFactory.create()
    new_name = "My place"
    auth_client.cookies["latitude"] = place.latitude
    auth_client.cookies["longitude"] = place.longitude
    response = auth_client.post(
        reverse_lazy("collector:update-place", kwargs={"pk": place.pk}),
        data={
            "name": new_name,
            "description": place.description,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_owner_can_see_place(
    user: User,
    auth_client,
) -> None:
    """Test owner can see place."""
    place = PlaceFactory.create(
        user=user,
    )
    response = auth_client.get(
        reverse_lazy(
            "collector:detail-place",
            kwargs={
                "pk": place.pk,
            },
        ),
    )
    assert response.status_code == status.HTTP_200_OK


def test_not_owner_can_see_place(
    auth_client,
) -> None:
    """Test not owner can see place."""
    place = PlaceFactory.create()
    response = auth_client.get(
        reverse_lazy(
            "collector:detail-place",
            kwargs={
                "pk": place.pk,
            },
        ),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
