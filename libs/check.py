from flask import redirect, session
from functools import wraps

def loggedout(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'login' not in session:
             return func(*args, **kwargs)
        else:
            return redirect('/')
    return wrapper

def loggedin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'login' in session:
             return func(*args, **kwargs)
        else:
            return redirect('/login')
    return wrapper

