from flask import Flask, redirect, url_for, request

from flask_login import current_user

from app.config import Config
from app.extensions import db, migrate, bcrypt, login_manager



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

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


    return app