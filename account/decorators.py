from django.http import HttpResponse
from django.shortcuts import redirect


def unauthendicated_user(view_func):
    '''
    To restrict who can acces which and proper restrictions,
    Only Unauthendicated Users can get acess further otherwise redirects
    '''
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('acc-home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    '''
    To restrict who can acces which and proper restrictions,
    Only users with roles are present in alowed_roles specified
    gets access further otherwise redirects
    '''
    def decorator(view_func):
        def wrapping_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized")
        return wrapping_func
    return decorator


def admin_only(view_func):
    '''
    To restrict who can acces which and proper restrictions,
    Only Authendicated Admin Users can get acess further otherwise redirects
    '''
    def wrapping_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():  # fetching group
            group = request.user.groups.all()[0].name

        if group == 'admin-group':
            return view_func(request, *args, **kwargs)
        elif group == 'user-group':
            return redirect('acc-home')
        else:
            return HttpResponse('You are not authorized :(    Error !')
    return wrapping_func
