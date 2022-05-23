from django.contrib import admin

from . import models


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    """Class representation Place model for admin panel."""

    search_fields = ("name",)
    list_display = (
        "id",
        "name",
        "description",
        "longitude",
        "latitude",
    )
