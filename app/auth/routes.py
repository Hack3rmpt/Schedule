from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, current_app
from app.models.user import User
from app.auth.forms import RegistrationForm, LoginForm

bp = Blueprint('auth', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        # Получаем доступ к базе данных через current_app
        db = current_app.extensions['sqlalchemy'].db
        db.session.add(user)
        db.session.commit()

        flash('Регистрация успешна. Теперь войдите в систему.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('auth.dashboard'))  # Редиректим в личный кабинет
        else:
            flash('Неверный email или пароль!', 'danger')

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('auth.login'))


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/dashboard.html', user=current_user)