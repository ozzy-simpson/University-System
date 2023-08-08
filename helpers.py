from functools import wraps
from flask import session, abort, redirect, url_for, request
import mysql.connector
import os

myDb = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    database="university_integrated"
)

def authorize(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'userType' not in session or session['userType'] not in roles:
                abort(401)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userId' not in session:
            # User is not logged in, so save the current route they're trying to access in the session
            session['next'] = request.url
            return redirect(url_for('login'))  # Redirect to the login page
        else:
            # User is logged in, so allow access to the requested route
            return f(*args, **kwargs)
    return decorated_function
