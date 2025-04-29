from flask import Flask, redirect, url_for, request

from flask_login import current_user

from app.config import Config
from app.extensions import db, migrate, bcrypt, login_manager,csrf
from app.models.user import User



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

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

    return app