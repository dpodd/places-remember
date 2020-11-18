from django.shortcuts import render, redirect
from .models import Memory
from .forms import MemoryModelForm
from django.contrib.auth.decorators import login_required
from .permissions import only_owner_can_access


@login_required
def profile_view(request, *args, **kwargs):
    queryset = Memory.objects.filter(user_id=request.user.id)
    form = MemoryModelForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect(request.path)

    context = {
        "memories": queryset,
        "form": form,
    }
    return render(request, 'profile.html', context)


@only_owner_can_access
def memory_view(request, *args, **kwargs):
    memory_obj = Memory.objects.get(slug=kwargs['slug'])
    context = {'memory': memory_obj}
    return render(request, 'memory_detail.html', context)
