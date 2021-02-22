from functools import wraps

from django.views.decorators.cache import cache_page
from django_hint import RequestType

__all__ = [
    "cache_for_user"
]


def cache_for_user(*func_args, **func_kwargs):
    """
    Cache for each user
    """
    
    def _controller(func):
        @wraps(func)
        def _wrapped_view_func(request: RequestType, *args, **kwargs):
            if request.GET.get("no-cache"):
                return func(request, *args, **kwargs)
            
            user_id = getattr(request.user, "id", "")
            key = user_id + func_kwargs.pop("key_prefix", "")
            
            return cache_page(*func_args, **func_kwargs, key_prefix=key)(func)(request, *args, **kwargs)
        
        return _wrapped_view_func
    
    return _controller
