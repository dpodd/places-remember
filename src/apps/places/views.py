from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render
from .models import Memory
from .forms import MemoryModelForm


def profile(request, *args, **kwargs):
    queryset = Memory.objects.filter(user_id=request.user.id)
    form = MemoryModelForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.title = form.cleaned_data.get('title')
        print(instance.title, flush=True)
        instance.user = request.user
        print(instance.user, flush=True)
        instance.description = form.cleaned_data.get('description')
        print(instance.description, flush=True)
        print(instance.location, flush=True)
        instance.location = 'Novosibirsk'
        print(instance.location, flush=True)
        instance.save()
        #instance.location = form.cleaned_data.get('location')


    context = {
        "message" : "Context has passed.",
        "memories" : queryset,
        "form" : form,
    }
    return render(request, 'home.html', context)


class HomePageView(TemplateView):
    template_name = "home.html"
