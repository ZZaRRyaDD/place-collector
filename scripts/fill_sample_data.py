from apps.collector import factories

PLACES_COUNT = 5


def run():
    """Generate examples of Place model."""
    factories.PlaceFactory.create_batch(size=PLACES_COUNT)
