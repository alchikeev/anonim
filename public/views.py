from django.contrib.flatpages.models import FlatPage
from django.views.generic import TemplateView


class FlatPageView(TemplateView):
    """Generic view to render a ``FlatPage`` instance."""

    template_name = "flatpage.html"
    url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = FlatPage.objects.get(url=self.url)
        return context


class HomeView(FlatPageView):
    url = "/"


class AboutView(FlatPageView):
    url = "/about/"


class ContactView(FlatPageView):
    url = "/contact/"

