from django.conf.urls import include
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required


def user_has_main_character(user):
    return bool(user.profile.main_character)


def decorate_url_patterns(urls, decorator):
    url_list, app_name, namespace = include(urls)

    def process_patterns(url_patterns):
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # this is an include - apply to all nested patterns
                process_patterns(pattern.url_patterns)
            else:
                # this is a pattern
                pattern.callback = decorator(pattern.callback)

    process_patterns(url_list)
    return url_list, app_name, namespace


def main_character_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if user_has_main_character(request.user):
            return view_func(request, *args, **kwargs)

        messages.error(request, _('A main character is required to perform that action. Add one below.'))
        return redirect('authentication:dashboard')
    return login_required(_wrapped_view)


def permissions_required(perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.

    This decorator is identical to the django permission_required except it
    allows for passing a tuple/list of perms that will return true if any one
    of them is present.
    """
    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        for perm_ in perms:
            perm_ = (perm_,)
            if user.has_perms(perm_):
                return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)
