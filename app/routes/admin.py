import os
import tarfile
import threading
from urllib.parse import quote_plus
from sqlalchemy.engine.url import make_url
import subprocess

from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, current_app, send_from_directory, \
    copy_current_request_context
from flask import Blueprint, session, send_file
from flask_login import login_required
from werkzeug.utils import secure_filename

from .decorators import admin_required
from app.forms import CreateUserForm, EditUserForm, DirectionForm, BackupForm
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
    log_level = request.args.get('level', 'INFO')  # Фильтр по уровню
    search_query = request.args.get('q', '')  # Поиск по тексту

    log_file = 'app.log'
    filtered_logs = []

    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            for line in f:
                # Фильтрация по уровню и поисковому запросу
                if log_level in line and search_query.lower() in line.lower():
                    filtered_logs.append(line)

    return render_template('admin/logs.html', logs=filtered_logs)

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


from pathlib import Path


def execute_command(command, shell=False):
    """Безопасное выполнение команд с логированием"""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300
        )
        current_app.logger.info(f"Command executed: {' '.join(command)}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed: {e.stderr}"
        current_app.logger.error(error_msg)
        raise RuntimeError(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        current_app.logger.error(error_msg)
        raise RuntimeError(error_msg)


@admin.route('/backup', methods=['GET', 'POST'])
@login_required
def backup_page():
    """Главная страница управления бэкапами"""
    backup_dir = get_backup_dir()
    backups = list_backups(backup_dir)

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'create':
            return create_backup()
        elif action == 'upload':
            return handle_upload()
        elif action == 'delete':
            filename = request.form.get('filename')
            return delete_backup(filename)

    return render_template('admin/backup.html', backups=backups)


def get_backup_dir():
    """Получаем директорию для хранения бэкапов"""
    backup_dir = os.path.join(current_app.root_path, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def list_backups(backup_dir):
    """Получаем список бэкапов с метаданными"""
    backups = []
    for filename in os.listdir(backup_dir):
        if filename.endswith('.sql'):
            filepath = os.path.join(backup_dir, filename)
            stat = os.stat(filepath)
            backups.append({
                'name': filename,
                'modified_time': datetime.fromtimestamp(stat.st_mtime),
                'size_mb': round(stat.st_size / (1024 * 1024), 2)
            })
    return sorted(backups, key=lambda x: x['modified_time'], reverse=True)


def create_backup():
    """Создание нового бэкапа базы данных"""
    backup_dir = get_backup_dir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"backup_{timestamp}.sql"
    backup_path = os.path.join(backup_dir, backup_filename)

    try:
        db_url = current_app.config['SQLALCHEMY_DATABASE_URI']

        # Создаем чистый дамп без команд очистки
        cmd = [
            'pg_dump',
            '--dbname', db_url,
            '-f', backup_path,
            '-F', 'p'  # plain text format
        ]

        execute_command(cmd)
        flash('Бэкап успешно создан', 'success')
    except Exception as e:
        flash(f'Ошибка при создании бэкапа: {str(e)}', 'danger')

    return redirect(url_for('admin.backup_page'))


def handle_upload():
    """Обработка загрузки файла бэкапа"""
    if 'file' not in request.files:
        flash('Файл не выбран', 'danger')
        return redirect(url_for('admin.backup_page'))

    file = request.files['file']
    if file.filename == '':
        flash('Файл не выбран', 'danger')
        return redirect(url_for('admin.backup_page'))

    if not allowed_file(file.filename):
        flash('Недопустимый формат файла', 'danger')
        return redirect(url_for('admin.backup_page'))

    backup_dir = get_backup_dir()
    filename = secure_filename(file.filename)
    backup_path = os.path.join(backup_dir, filename)

    try:
        file.save(backup_path)

        # Используем копию контекста запроса для потока
        @copy_current_request_context
        def restore_wrapper():
            db_url = current_app.config['SQLALCHEMY_DATABASE_URI']
            try:
                restore_database(backup_path, db_url)
                flash('База данных успешно восстановлена', 'success')
            except Exception as e:
                flash(f'Ошибка восстановления: {str(e)}', 'danger')

        thread = threading.Thread(target=restore_wrapper)
        thread.start()

        flash('Восстановление запущено. Пожалуйста, подождите.', 'info')
    except Exception as e:
        flash(f'Ошибка при загрузке файла: {str(e)}', 'danger')

    return redirect(url_for('admin.backup_page'))


def restore_database(backup_path, db_url):
    """Восстановление базы данных из бэкапа"""
    try:
        current_app.logger.info("Starting database restore...")

        # Создаем временный файл скрипта
        temp_script = f"""
        \\set ON_ERROR_STOP on
        DROP SCHEMA IF EXISTS public CASCADE;
        CREATE SCHEMA public;
        \\i {backup_path}
        """

        temp_path = os.path.join(os.path.dirname(backup_path), "temp_restore.sql")
        with open(temp_path, 'w') as f:
            f.write(temp_script)

        # Выполняем восстановление
        cmd = [
            'psql',
            '--dbname', db_url,
            '-v', 'ON_ERROR_STOP=1',
            '-f', temp_path
        ]

        execute_command(cmd)
        os.remove(temp_path)
        current_app.logger.info("Database restored successfully")
    except Exception as e:
        current_app.logger.error(f"Restore failed: {str(e)}")
        raise


def delete_backup(filename):
    """Удаление файла бэкапа"""
    backup_dir = get_backup_dir()
    backup_path = os.path.join(backup_dir, secure_filename(filename))

    try:
        if os.path.exists(backup_path):
            os.remove(backup_path)
            flash('Бэкап успешно удален', 'success')
        else:
            flash('Файл не найден', 'warning')
    except Exception as e:
        flash(f'Ошибка при удалении: {str(e)}', 'danger')

    return redirect(url_for('admin.backup_page'))


@admin.route('/backup/download/<filename>')
@login_required
def download_backup(filename):
    """Скачивание файла бэкапа"""
    backup_dir = get_backup_dir()
    backup_path = os.path.join(backup_dir, secure_filename(filename))

    if not os.path.exists(backup_path):
        flash('Файл бэкапа не найден', 'danger')
        return redirect(url_for('admin.backup_page'))

    return send_file(backup_path, as_attachment=True)


def allowed_file(filename):
    """Проверка разрешенных расширений файлов"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'sql'