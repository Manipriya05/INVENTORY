from functools import wraps

from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.utils.http import urlencode
from django.http import HttpResponseRedirect


def staff_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = resolve_url('login')
            query = urlencode({'next': request.get_full_path()})
            return HttpResponseRedirect(f'{login_url}?{query}')
        if not request.user.is_active or not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped
