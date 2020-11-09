from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render
from .models import Memory


def profile(request, *args, **kwargs):
    queryset = Memory.objects.filter(user_id=request.user.id)
    print(queryset, flush=True)

    context = {
        "message" : "Context has passed.",
        "memories" : queryset,
    }
    return render(request, 'home.html', context)


class HomePageView(TemplateView):
    template_name = "home.html"
