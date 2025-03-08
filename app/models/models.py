from app.extensions import db, bcrypt
from datetime import datetime

### 2. Таблица предметов ###
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


### 3. Таблица групп студентов ###
class StudentGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


### 4. Таблица преподавателей ###
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


### 5. Таблица аудиторий ###
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)


### 6. Таблица экзаменов ###
class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('student_group.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    subject = db.relationship('Subject', backref=db.backref('exams', lazy=True))
    group = db.relationship('StudentGroup', backref=db.backref('exams', lazy=True))
    teacher = db.relationship('Teacher', backref=db.backref('exams', lazy=True))
    room = db.relationship('Room', backref=db.backref('exams', lazy=True))


### 7. Таблица параметров генерации расписания ###
class ScheduleSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    exams_per_day = db.Column(db.Integer, default=2)
    max_exams_per_group = db.Column(db.Integer, default=1)


### 8. Таблица логов изменений расписания ###
class ScheduleLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=False)  # Например, "Добавлен экзамен", "Удалён экзамен"
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Кто сделал изменение

    user = db.relationship('User', backref=db.backref('logs', lazy=True))