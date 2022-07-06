from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
def user_passes_test(
    test_func,model_obj=None,raise_exception=False,url_input_obj_name=None
):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user,model_obj,kwargs): # kwargs contains the given variable in the url
                return view_func(request, *args, **kwargs)
            if raise_exception:
                raise PermissionDenied

        return _wrapped_view

    return decorator

