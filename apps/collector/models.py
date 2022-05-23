from django.db import models
from django.utils.translation import gettext_lazy as _


class Place(models.Model):
    """Model for place."""

    latitude = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Latitude place"),
    )
    longitude = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Longitude place"),
    )
    name = models.CharField(
        max_length=128,
        verbose_name=_("Name place"),
    )
    description = models.TextField(
        verbose_name=_("Description of place"),
    )

    def __str__(self) -> str:
        """Return info about model."""
        return self.name

    class Meta:
        verbose_name_plural = _("Places")
        verbose_name = _("Place")
