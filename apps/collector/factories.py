import factory

from apps.users.factories import UserFactory

from . import models


class PlaceFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Place instance."""

    latitude = factory.Faker(
        "latitude",
    )
    longitude = factory.Faker(
        "longitude",
    )
    description = factory.Faker(
        "catch_phrase",
    )
    name = factory.Faker(
        "currency_name",
    )
    user = factory.SubFactory(
        UserFactory,
    )

    class Meta:
        model = models.Place
