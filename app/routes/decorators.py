from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Доступ запрещен. Требуются права администратора.', 'danger')
            return redirect(url_for('main.index'))  # Перенаправляем на главную страницу
        return func(*args, **kwargs)
    return decorated_view