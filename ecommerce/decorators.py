from django.shortcuts import redirect
from functools import wraps

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'custom_user_id' not in request.session:
            return redirect('custom_login')  # Your custom login view name
        return view_func(request, *args, **kwargs)
    return wrapper
