from django.views.generic import ListView, TemplateView

class ListPlacesView(TemplateView):
    template_name = "collector/list_places.html"
