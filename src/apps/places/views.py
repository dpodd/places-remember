from django.http import HttpResponse
from django.views.generic.base import TemplateView


def profile(request, *args, **kwargs):
    html = "<html><body>Places app placeholder</body></html>"
    return HttpResponse(html)


class HomePageView(TemplateView):
    template_name = "home.html"
