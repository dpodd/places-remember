from django.shortcuts import render
from .models import Memory
from .forms import MemoryModelForm


def profile_view(request, *args, **kwargs):
    queryset = Memory.objects.filter(user_id=request.user.id)
    form = MemoryModelForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()

    context = {
        "memories": queryset,
        "form": form,
    }
    return render(request, 'profile.html', context)


def memory_view(request, *args, **kwargs):
    memory_obj = Memory.objects.get(slug=kwargs['slug'])
    context = {'memory': memory_obj}
    return render(request, 'memory_detail.html', context)
