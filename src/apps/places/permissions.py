import functools
from .models import Memory
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


def only_owner_can_access(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        slug = kwargs.get('slug')
        if not request.user.is_authenticated:
            raise PermissionDenied
        user_id = request.user.id
        obj = get_object_or_404(Memory, slug=slug)

        if obj.user_id == user_id:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper
