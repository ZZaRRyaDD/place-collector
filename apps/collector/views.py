from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models


class ListPlacesView(generic.ListView):
    """View for list of places."""

    template_name = "collector/list_places.html"
    queryset = models.Place.objects.all()
    context_object_name = "places"


class AddPlaceView(generic.CreateView):
    """View for Place create."""

    template_name = "collector/add_places.html"
    queryset = models.Place.objects.all()
    model = models.Place
    form_class = forms.PlaceForm

    def get_success_url(self) -> str:
        """Get url for reverse after success create."""
        return reverse_lazy("collector:list-places")

    def post(self, request, *args, **kwargs):
        """Handler for POST request."""
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(
                form,
                request.COOKIES["latitude"],
                request.COOKIES["longitude"],
                request.user,
            )
        return self.form_invalid(form)

    def form_valid(self, form, latitude, longitude, user):
        """Overridden for save form after create."""
        object = form.save(commit=False)
        object.latitude = latitude
        object.longitude = longitude
        object.user = user
        object.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """Overridden for reload context for retry create."""
        return self.render_to_response(
            self.get_context_data(form=form),
        )


class DetailPlaceView(generic.DetailView):
    """View for detail information about place."""

    queryset = models.Place.objects.all()
    template_name = "collector/detail_place.html"
    context_object_name = "place"


class DeletePlaceView(generic.DeleteView):
    """View for delete place."""

    model = models.Place

    def get_success_url(self) -> str:
        """Get url for reverse after delete place."""
        return reverse_lazy("collector:list-places")


class UpdatePlaceView(generic.UpdateView):
    """View for update place."""

    template_name = "collector/update_place.html"
    form_class = forms.PlaceForm
    queryset = models.Place.objects.all()
    context_object_name = "place"

    def get_success_url(self) -> str:
        """Get url for reverse after delete place."""
        return reverse_lazy(
            "collector:detail-place",
            kwargs={"pk": self.get_object().pk},
        )

    def get_object(self):
        """Get object those will be update."""
        return self.queryset.get(id=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        """Handler for POST request."""
        form = forms.PlaceForm(
            request.POST,
            instance=self.get_object(),
        )
        if form.is_valid():
            return self.form_valid(
                form,
                request.COOKIES["latitude"],
                request.COOKIES["longitude"],
                request.user,
            )
        return self.form_invalid(form)

    def form_valid(self, form, latitude, longitude, user):
        """Overridden for save form after update."""
        object = form.save(commit=False)
        object.latitude = latitude
        object.longitude = longitude
        object.user = user
        object.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """Overriden for reload page"""
        return self.render_to_response(self.get_context_data(form=form))
