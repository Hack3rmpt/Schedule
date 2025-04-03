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


### 3. Модифицированная таблица групп ###
class StudentGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)  # Исправлено на 'course.id'
    course = db.relationship('Course', back_populates='groups')  # Связь с моделью Course
    exams = db.relationship('Exam', back_populates='group')


### Смежная
teacher_subject = db.Table('teacher_subject',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key=True)
)
### 4. Таблица предметов (без изменений)
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    assessment_type = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    # Связь с учителями
    teachers = db.relationship('Teacher', secondary=teacher_subject, back_populates='subjects')

    __table_args__ = (
        db.UniqueConstraint('name', 'course_id', name='unique_subject_name_per_course'),
    )


### 5. Таблица преподавателей (без изменений) ###
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Связь с предметами
    subjects = db.relationship('Subject', secondary=teacher_subject, back_populates='teachers')

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name]
        if self.patronymic:
            parts.append(self.patronymic)
        return ' '.join(parts)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    specialization_id = db.Column(db.Integer, db.ForeignKey('specialization.id'), nullable=False)
    specialization = db.relationship('Specialization', backref=db.backref('courses', lazy=True))
    groups = db.relationship('StudentGroup', back_populates='course')  # Добавьте связь с группами
    subjects = db.relationship('Subject', backref='course', lazy='dynamic')
    def __repr__(self):
        return f'<Course {self.number}>'



### 6. Таблица аудиторий (добавлен тип аудитории) ###
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), default='lecture')  # lecture/practice/lab
    building = db.Column(db.String(50), default='Корпус на ул. Нежинской 7')

    @property
    def full_number(self):
        return f"{self.number} ({self.type})"


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

    # Свойство для получения курса через группу
    @property
    def course(self):
        return self.group.course


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