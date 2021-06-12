from flask import redirect, url_for, flash
from functools import wraps
from flask_login import current_user

def check_logged(my_func):
    @wraps(my_func)
    def wrapper_func(*args, **kwargs):
        if current_user.is_authenticated:
            flash('Can´t access that page while logged in', category='error')
            return redirect(url_for('views.index'))
        return my_func(*args, **kwargs)  
    return wrapper_func
