from functools import wraps

from flask import flash, redirect, session, url_for

from extensions import db
from models import User


def current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return db.session.get(User, user_id)


def login_required(role=None):
    """Route decorator that enforces login, and optionally a specific role.

    Usage:
        @login_required()            -> any logged-in, non-blacklisted user
        @login_required(role='admin') -> must also have that role
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = session.get('user_id')
            if not user_id:
                flash('Please login first.', 'warning')
                return redirect(url_for('auth.login'))
            user = db.session.get(User, user_id)
            if not user or user.blacklisted:
                session.clear()
                flash('Access denied.', 'danger')
                return redirect(url_for('auth.login'))
            if role and user.role != role:
                flash('You are not authorized to access this page.', 'danger')
                return redirect(url_for('main.dashboard'))
            return func(*args, **kwargs)
        return wrapper
    return decorator