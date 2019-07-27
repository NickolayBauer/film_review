from functools import wraps, partial

from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from main.models import User


def anonymous_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        return function(request, *args, **kwargs)
    return wrap
