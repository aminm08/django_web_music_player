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

# the test func for the above decorator
def check_user_and_adder(user,model_object,url_info): # url_info_containts the kwargs

    url_object_name = list(url_info.keys())[0]
    url_object_value = url_info.get(url_object_name)
    # get the object depended on url variable name
    if url_object_name == 'pk':
        obj = get_object_or_404(model_object,pk=url_object_value)
    elif url_object_name == 'playlist_name':
        obj = get_object_or_404(model_object,playlist_name=url_object_value)
    return user == obj.user # true if this user is the same user in DB
