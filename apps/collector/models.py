from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class Place(models.Model):
    """Model for place."""

    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(
        max_length=128,
        verbose_name=_("Name place"),
    )
    description = models.TextField(
        verbose_name=_("Description of place"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Owner of post about place"),
    )

    def __str__(self) -> str:
        """Return info about model."""
        return self.name

    class Meta:
        verbose_name_plural = _("Places")
        verbose_name = _("Place")
