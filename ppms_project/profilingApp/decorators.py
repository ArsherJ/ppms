from django.http import HttpResponse
from django.shortcuts import redirect, render

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        
        if request.user.is_authenticated and request.user.user_type == 'P/G':
            return redirect('parent_home')
        elif request.user.is_authenticated and request.user.user_type == 'BHW':
            return redirect('bhw_home')
        elif request.user.is_authenticated and request.user.user_type == 'Admin':
            return redirect('admin_home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func