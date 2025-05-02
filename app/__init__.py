from flask import Flask, redirect, url_for, request

from flask_login import current_user

from app.config import Config
from app.extensions import db, migrate, bcrypt, login_manager,csrf
from app.models.user import User
import logging
from logging.handlers import RotatingFileHandler
from flask_mail import Mail, Message

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'isip_d.s.kuznecov@mpt.ru'  # Замените на ваш email
    app.config['MAIL_PASSWORD'] = 'otmy ydpy vfzs pukd'  # Замените на ваш пароль
    app.config['MAIL_DEFAULT_SENDER'] = 'isip_d.s.kuznecov@mpt.ru'
    mail.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf.init_app(app)

    from app.auth.routes import auth
    from app.routes.admin import admin
    from app.routes.main import main
    from app.routes.schedule import schedule
    # Регистрация Blueprint
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(main)
    app.register_blueprint(schedule, url_prefix='/schedule')

    with app.app_context():
        db.create_all()

        admin_user = User.query.filter_by(role='admin').first()
        if not admin_user:
            admin = User(
                username="admin",
                email="admin@example.com",
                role="admin"  # Роль
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("Суперпользователь создан: admin@example.com / admin123")

    app.logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.info('=== Application started ===')

    return app

def send_schedule_email(app, recipient, schedule_data):
    with app.app_context():
        msg = Message("Расписание экзаменов", recipients=[recipient])
        msg.body = "Вот ваше расписание:\n\n" + schedule_data
        mail.send(msg)