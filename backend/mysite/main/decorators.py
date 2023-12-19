from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wraper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                for group in request.user.groups.all():
                    if group.name in allowed_roles:
                        return view_func(request, *args, **kwargs)
                    else:
                        return HttpResponse('You are not authorize to view this page')
            else:
                return HttpResponse('You are not authorize to view this page')
        return wraper_func
    return decorator