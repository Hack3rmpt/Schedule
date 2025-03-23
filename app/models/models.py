from app.extensions import db, bcrypt
from datetime import datetime


### 1. Таблица направлений ###
class Direction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # "09.02.07"
    name = db.Column(db.String(100), nullable=False)  # "Информационные системы"
    specializations = db.relationship('Specialization', back_populates='direction', cascade='all, delete-orphan')


### 2. Таблица специальностей ###
class Specialization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # "Программист"
    direction_id = db.Column(db.Integer, db.ForeignKey('direction.id'), nullable=False)
    direction = db.relationship('Direction', back_populates='specializations')
    groups = db.relationship('StudentGroup', back_populates='specialization')


### 3. Модифицированная таблица групп ###
class StudentGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'), nullable=False)
    specialization = db.relationship('Specialization', back_populates='groups')
    exams = db.relationship('Exam', back_populates='group')


### 4. Таблица предметов (без изменений) ###
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


### 5. Таблица преподавателей (без изменений) ###
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


### 6. Таблица аудиторий (добавлен тип аудитории) ###
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), default='lecture')  # lecture/practice/lab


### 7. Модифицированная таблица экзаменов ###
class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)  # объединенные дата и время
    duration = db.Column(db.Integer, default=90)  # длительность в минутах

    # Связи
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('student_group.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    # Relationships
    subject = db.relationship('Subject', backref=db.backref('exams', lazy=True))
    group = db.relationship('StudentGroup', back_populates='exams')
    teacher = db.relationship('Teacher', backref=db.backref('exams', lazy=True))
    room = db.relationship('Room', backref=db.backref('exams', lazy=True))


### 8. Модифицированные настройки (привязка к направлению) ###
class ScheduleSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    direction_id = db.Column(db.Integer, db.ForeignKey('direction.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    max_exams_per_day = db.Column(db.Integer, default=3)
    min_days_between_exams = db.Column(db.Integer, default=2)

    direction = db.relationship('Direction', backref=db.backref('settings', uselist=False))


### 9. Таблица логов (добавлена привязка к направлению) ###
class ScheduleLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    direction_id = db.Column(db.Integer, db.ForeignKey('direction.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    direction = db.relationship('Direction', backref=db.backref('logs', lazy=True))
    user = db.relationship('User', backref=db.backref('logs', lazy=True))