import pytest
from django.test.client import Client

from apps.users.factories import UserFactory
from apps.users.models import User


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(django_db_setup, django_db_blocker):
    """Module-level fixture for user."""
    with django_db_blocker.unblock():
        created_user = UserFactory()
        yield created_user
        created_user.delete()


@pytest.fixture
def auth_client(user: User, client: Client):
    """Fixture for authtorized client."""
    client.force_login(user=user)
    return client
