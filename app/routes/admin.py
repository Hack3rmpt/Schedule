from flask import render_template, redirect, url_for, flash, request
from flask import Blueprint
from flask_login import login_required

from .decorators import admin_required
from app.forms import CreateUserForm, EditUserForm, DirectionForm
from app.models.user import User
from app.models.models import Specialization, Direction
from app.extensions import db

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/logs')
@login_required
@admin_required
def logs():
    return render_template('admin/logs.html')

@admin.route('/create_user', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    form = CreateUserForm()
    users = User.query.all()

    if users is None:
        users = []

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Пользователь успешно создан!', 'success')
        return redirect(url_for('admin.create_user'))

    return render_template('admin/create_user.html', form=form, users=users, edit_form=EditUserForm())


@admin.route('/edit_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(request.form)  # Передаем данные запроса

    if form.validate_on_submit():
        if int(form.user_id.data) != user.id:
            flash('Несоответствие идентификаторов', 'danger')
            return redirect(url_for('admin.create_user'))

        # Обновление данных
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data

        # Обновление пароля
        if form.password.data:
            user.set_password(form.password.data)

        db.session.commit()
        flash('Изменения сохранены!', 'success')
    else:
        # Логирование ошибок валидации
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {field}: {error}', 'danger')

    return redirect(url_for('admin.create_user'))

@admin.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Нельзя удалить администратора!', 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь удален!', 'success')
    return redirect(url_for('admin.create_user'))








