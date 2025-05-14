from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
import os

# Добавляем путь к проекту в sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем экземпляр SQLAlchemy и модели
from app import create_app  # Если у вас есть функция create_app()
from app.extensions import db
from app.models.models import Direction, Specialization, StudentGroup, Subject, Teacher, Course, Room, Exam, ScheduleSettings, ScheduleLog  # Импорт всех моделей

app = create_app()  # Создаем экземпляр приложения
config = context.config

# Связываем метаданные SQLAlchemy с конфигом Alembic
target_metadata = db.Model.metadata

def run_migrations_offline():
    url = app.config['SQLALCHEMY_DATABASE_URI']
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = db.engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Обернем в контекст приложения
with app.app_context():
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
