from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, HiddenField, DateField, DateTimeField, IntegerField
from wtforms.fields.choices import RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, NumberRange
from app.models.user import User

from app.models.models import Direction, Specialization, StudentGroup, Subject, Teacher, Room, Course
from datetime import datetime

class CreateUserForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=3, max=64, message="Имя пользователя должно быть от 3 до 64 символов")
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Введите корректный email")
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6, message="Пароль должен быть не менее 6 символов")
    ])
    confirm_password = PasswordField('Повторите пароль', validators=[
        DataRequired(),
        EqualTo('password', message="Пароли должны совпадать")
    ])
    role = SelectField('Роль', choices=[
        ('admin', 'Администратор'),
        ('worker', 'Сотрудник')
    ], validators=[DataRequired()])
    submit = SubmitField('Создать пользователя')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован')



class EditUserForm(FlaskForm):
    user_id = HiddenField('ID пользователя', validators=[DataRequired()])
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль',
                                   validators=[EqualTo('password', message='Пароли должны совпадать'), Optional()])
    role = SelectField('Роль', choices=[('admin', 'Админ'), ('worker', 'Работник')], validators=[DataRequired()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and user.id != int(self.user_id.data):
            raise ValidationError('Email уже используется')



class DirectionForm(FlaskForm):
    code = StringField('Код направления', validators=[
        DataRequired(),
        Length(max=20, message="Максимум 20 символов")
    ])
    name = StringField('Название направления', validators=[
        DataRequired(),
        Length(max=100, message="Максимум 100 символов")
    ])
    submit = SubmitField('Сохранить')

    def __init__(self, current_id=None, *args, **kwargs):
        super(DirectionForm, self).__init__(*args, **kwargs)
        self.current_id = current_id

    def validate_code(self, field):
        query = Direction.query.filter_by(code=field.data)
        if self.current_id:
            query = query.filter(Direction.id != self.current_id)
        if query.first():
            raise ValidationError('Направление с таким кодом уже существует')

### 2. Формы для специальности (Specialization) ###
class AddSpecializationForm(FlaskForm):
    name = StringField('Название специальности', validators=[
        DataRequired(),
        Length(max=100, message="Максимум 100 символов")
    ])
    direction_id = SelectField('Направление', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить специальность')

    def __init__(self, *args, **kwargs):
        super(AddSpecializationForm, self).__init__(*args, **kwargs)
        self.direction_id.choices = [(d.id, d.name) for d in Direction.query.all()]

    def validate_name(self, field):
        if Specialization.query.filter_by(name=field.data).first():
            raise ValidationError('Специальность с таким названием уже существует')

class EditSpecializationForm(FlaskForm):
    specialization_id = HiddenField('ID специальности')
    name = StringField('Название специальности', validators=[
        DataRequired(),
        Length(max=100, message="Максимум 100 символов")
    ])
    direction_id = SelectField('Направление', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения')

    def __init__(self, *args, **kwargs):
        super(EditSpecializationForm, self).__init__(*args, **kwargs)
        self.direction_id.choices = [(d.id, d.name) for d in Direction.query.all()]

    def validate_name(self, field):
        specialization = Specialization.query.filter_by(name=field.data).first()
        if specialization and specialization.id != int(self.specialization_id.data):
            raise ValidationError('Специальность с таким названием уже существует')

from wtforms import SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class AddCourseForm(FlaskForm):
    number = SelectField(
        'Номер курса',
        coerce=int,
        choices=[(1, '1 курс'), (2, '2 курс'), (3, '3 курс'), (4, '4 курс')],
        validators=[DataRequired(message="Выберите номер курса")]
    )
    submit = SubmitField('Добавить курс')

    def validate_number(self, field):
        # Получаем specialization_id из URL параметров
        specialization_id = request.view_args.get('specialization_id')

        if not specialization_id:
            raise ValidationError('Специальность не определена')

        if Course.query.filter_by(
                number=field.data,
                specialization_id=specialization_id
        ).first():
            raise ValidationError('Курс с таким номером уже существует для этой специальности')


class EditCourseForm(FlaskForm):
    course_id = HiddenField('ID курса')
    number = SelectField(
        'Номер курса',
        coerce=int,
        choices=[(1, '1 курс'), (2, '2 курс'), (3, '3 курс'), (4, '4 курс')],
        validators=[DataRequired(message="Выберите номер курса")]
    )
    submit = SubmitField('Сохранить изменения')

    def validate_number(self, field):
        course = Course.query.get(int(self.course_id.data))
        if course and course.number != field.data:
            existing = Course.query.filter_by(
                number=field.data,
                specialization_id=course.specialization_id
            ).first()
            if existing:
                raise ValidationError('Курс с таким номером уже существует для этой специальности')

from wtforms import SelectMultipleField

class AddSubjectForm(FlaskForm):
    name = StringField(
        'Название предмета',
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )
    course_id = SelectField(
        'Курс',
        coerce=int,
        validators=[DataRequired()]
    )
    assessment_type = SelectField(
        'Тип аттестации',
        choices=[('Экзамен', 'Экзамен'), ('Зачет', 'Зачет')],
        validators=[DataRequired()]
    )
    teachers = SelectMultipleField(
        'Преподаватели',
        coerce=int,
        validators=[DataRequired()]
    )
    submit = SubmitField('Добавить')

    def validate_name(self, field):
        if Subject.query.filter_by(
            name=field.data,
            course_id=self.course_id.data
        ).first():
            raise ValidationError('Предмет уже существует для этого курса')


class EditSubjectForm(FlaskForm):
    subject_id = HiddenField()
    name = StringField(
        'Название предмета',
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )
    course_id = SelectField(
        'Курс',
        coerce=int,
        validators=[DataRequired()]
    )
    assessment_type = SelectField(
        'Тип аттестации',
        choices=[('Экзамен', 'Экзамен'), ('Зачет', 'Зачет')],
        validators=[DataRequired()]
    )
    teachers = SelectMultipleField(
        'Преподаватели',
        coerce=int,
        validators=[DataRequired()]
    )
    submit = SubmitField('Обновить')

    def validate_name(self, field):
        subject = Subject.query.filter_by(
            name=field.data,
            course_id=self.course_id.data
        ).first()
        if subject and subject.id != int(self.subject_id.data):
            raise ValidationError('Название предмета должно быть уникальным для курса')


### 3. Формы для группы (StudentGroup) ###
class AddGroupForm(FlaskForm):
    name = StringField('Название группы', validators=[
        DataRequired(),
        Length(max=50, message="Максимум 50 символов")
    ])
    course_id = SelectField('Курс', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить группу')

    def validate_name(self, field):
        group = StudentGroup.query.filter_by(name=field.data).first()
        if group:
            raise ValidationError('Группа с таким названием уже существует')


class EditGroupForm(FlaskForm):
    group_id = HiddenField('ID группы')
    name = StringField('Название группы', validators=[
        DataRequired(),
        Length(max=50, message="Максимум 50 символов")
    ])
    course_id = SelectField('Курс', coerce=int, validators=[DataRequired()])  # Замените specialization_id на course_id
    submit = SubmitField('Сохранить изменения')

    def __init__(self, *args, **kwargs):
        super(EditGroupForm, self).__init__(*args, **kwargs)
        self.course_id.choices = [(c.id, f"{c.number} курс") for c in Course.query.all()]  # Обновите выбор курсов

    def validate_name(self, field):
        group = StudentGroup.query.filter_by(name=field.data).first()
        if group and group.id != int(self.group_id.data):
            raise ValidationError('Группа с таким названием уже существует')

### 4. Формы для аудитории (Room) ###
class AddRoomForm(FlaskForm):
    number = StringField('Номер аудитории', validators=[
        DataRequired(),
        Length(max=10, message="Максимум 10 символов")
    ])
    capacity = IntegerField('Вместимость', validators=[
        DataRequired(),
        NumberRange(min=1, max=1000, message="Допустимые значения 1-1000")
    ])
    type = SelectField('Тип аудитории', choices=[
        ('lecture', 'Лекционная'),
        ('practice', 'Практическая'),
        ('lab', 'Лаборатория')
    ], validators=[DataRequired()])
    building = SelectField('Корпус', choices=[
        ('Корпус на ул. Нежинской 7', 'Корпус на ул. Нежинской 7'),
        ('Корпус на ул. Нахимовский проспект 21', 'Корпус на ул. Нахимовский проспект 21')
    ], validators=[DataRequired()])
    submit = SubmitField('Добавить аудиторию')

    def validate_number(self, field):
        if Room.query.filter_by(number=field.data).first():
            raise ValidationError('Аудитория с таким номером уже существует')


class EditRoomForm(FlaskForm):
    room_id = HiddenField('ID аудитории', validators=[DataRequired()])  # Добавлен валидатор
    number = StringField('Номер аудитории', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Length(max=10, message="Максимум 10 символов")
    ])
    capacity = IntegerField('Вместимость', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        NumberRange(min=1, max=1000, message="Допустимые значения 1-1000")
    ])
    type = SelectField('Тип аудитории', choices=[
        ('lecture', 'Лекционная'),
        ('practice', 'Практическая'),
        ('lab', 'Лаборатория')
    ], validators=[DataRequired(message="Выберите тип аудитории")])
    building = SelectField('Корпус', choices=[
        ('Корпус на ул. Нежинской 7', 'Корпус на ул. Нежинской 7'),
        ('Корпус на ул. Нахимовский проспект 21', 'Корпус на ул. Нахимовский проспект 21')
    ], validators=[DataRequired(message="Выберите корпус")])
    submit = SubmitField('Сохранить изменения')

    def validate_number(self, field):
        # Проверяем, что room_id.data существует и является числом
        try:
            room_id = int(self.room_id.data) if self.room_id.data else None
        except ValueError:
            raise ValidationError('Неверный идентификатор аудитории')

        room = Room.query.filter_by(number=field.data).first()
        if room and room.id != room_id:
            raise ValidationError('Аудитория с таким номером уже существует')



### 5. Формы для экзамена (Exam) ###
# class AddExamForm(FlaskForm):
#     datetime = DateTimeField('Дата и время', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
#     duration = IntegerField('Длительность (минуты)', validators=[
#         DataRequired(),
#         NumberRange(min=1, max=240, message="Допустимые значения 1-240")
#     ])
#     subject_id = SelectField('Предмет', coerce=int, validators=[DataRequired()])
#     group_id = SelectField('Группа', coerce=int, validators=[DataRequired()])
#     teacher_id = SelectField('Преподаватель', coerce=int, validators=[DataRequired()])
#     room_id = SelectField('Аудитория', coerce=int, validators=[DataRequired()])
#     submit = SubmitField('Добавить экзамен')
#
#     def __init__(self, *args, **kwargs):
#         super(AddExamForm, self).__init__(*args, **kwargs)
#         self.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
#         self.group_id.choices = [(g.id, g.name) for g in StudentGroup.query.all()]
#         self.teacher_id.choices = [(t.id, t.full_name) for t in Teacher.query.all()]
#         self.room_id.choices = [(r.id, f"{r.number} ({r.type})") for r in Room.query.all()]
#
# class EditExamForm(FlaskForm):
#     exam_id = HiddenField('ID экзамена')
#     datetime = DateTimeField('Дата и время', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
#     duration = IntegerField('Длительность (минуты)', validators=[
#         DataRequired(),
#         NumberRange(min=1, max=240, message="Допустимые значения 1-240")
#     ])
#     subject_id = SelectField('Предмет', coerce=int, validators=[DataRequired()])
#     group_id = SelectField('Группа', coerce=int, validators=[DataRequired()])
#     teacher_id = SelectField('Преподаватель', coerce=int, validators=[DataRequired()])
#     room_id = SelectField('Аудитория', coerce=int, validators=[DataRequired()])
#     submit = SubmitField('Сохранить изменения')
#
#     def __init__(self, exam=None, *args, **kwargs):  # Добавьте параметр exam
#         super(EditExamForm, self).__init__(*args, **kwargs)
#         self.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
#         self.group_id.choices = [(g.id, g.name) for g in StudentGroup.query.all()]
#         self.teacher_id.choices = [(t.id, t.full_name) for t in Teacher.query.all()]
#         self.room_id.choices = [(r.id, f"{r.number} ({r.type})") for r in Room.query.all()]
#
#         if exam:  # Заполняем данные формы из объекта экзамена
#             self.datetime.data = exam.datetime
#             self.duration.data = exam.duration
#             self.subject_id.data = exam.subject_id
#             self.group_id.data = exam.group_id
#             self.teacher_id.data = exam.teacher_id
#             self.room_id.data = exam.room_id

class AddExamForm(FlaskForm):
    datetime = DateTimeField('Дата и время', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    duration = IntegerField('Длительность (минуты)', validators=[
        DataRequired(),
        NumberRange(min=1, max=240, message="Допустимые значения 1-240")
    ])
    subject_id = SelectField('Предмет', coerce=int, validators=[DataRequired()])
    group_id = SelectField('Группа', coerce=int, validators=[DataRequired()])
    teacher_id = SelectField('Преподаватель', coerce=int, validators=[DataRequired()])
    room_id = SelectField('Аудитория', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить экзамен')

    def __init__(self, *args, **kwargs):
        super(AddExamForm, self).__init__(*args, **kwargs)
        self.subject_id.choices = [(s.id, s.name) for s in Subject.query.order_by(Subject.name).all()]
        self.group_id.choices = [(g.id, g.name) for g in StudentGroup.query.order_by(StudentGroup.name).all()]
        self.teacher_id.choices = [(t.id, t.full_name) for t in Teacher.query.order_by(Teacher.last_name).all()]
        self.room_id.choices = [(r.id, f"{r.number} ({r.type})") for r in Room.query.order_by(Room.number).all()]


class EditExamForm(FlaskForm):
    datetime = DateTimeField('Дата и время', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    duration = IntegerField('Длительность (минуты)', validators=[
        DataRequired(),
        NumberRange(min=1, max=240, message="Допустимые значения 1-240")
    ])
    subject_id = SelectField('Предмет', coerce=int, validators=[DataRequired()])
    group_id = SelectField('Группа', coerce=int, validators=[DataRequired()])
    teacher_id = SelectField('Преподаватель', coerce=int, validators=[DataRequired()])
    room_id = SelectField('Аудитория', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения')

    def __init__(self, *args, **kwargs):
        exam = kwargs.pop('exam', None)
        super(EditExamForm, self).__init__(*args, **kwargs)

        self.subject_id.choices = [(s.id, s.name) for s in Subject.query.order_by(Subject.name).all()]
        self.group_id.choices = [(g.id, g.name) for g in StudentGroup.query.order_by(StudentGroup.name).all()]
        self.teacher_id.choices = [(t.id, t.full_name) for t in Teacher.query.order_by(Teacher.last_name).all()]
        self.room_id.choices = [(r.id, f"{r.number} ({r.type})") for r in Room.query.order_by(Room.number).all()]

        if exam:
            self.datetime.data = exam.datetime
            self.duration.data = exam.duration
            self.subject_id.data = exam.subject_id
            self.group_id.data = exam.group_id
            self.teacher_id.data = exam.teacher_id
            self.room_id.data = exam.room_id





### 6. Формы для настроек расписания (ScheduleSettings) ###
class AddScheduleSettingsForm(FlaskForm):
    direction_id = SelectField('Направление', coerce=int, validators=[DataRequired()])
    start_date = DateField('Дата начала', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Дата окончания', format='%Y-%m-%d', validators=[DataRequired()])
    max_exams_per_day = IntegerField('Максимум экзаменов в день', validators=[
        DataRequired(),
        NumberRange(min=1, max=10, message="Допустимые значения 1-10")
    ])
    min_days_between_exams = IntegerField('Минимальный интервал между экзаменами', validators=[
        DataRequired(),
        NumberRange(min=1, max=10, message="Допустимые значения 1-10")
    ])
    submit = SubmitField('Добавить настройки')

    def validate_end_date(self, field):
        if field.data < self.start_date.data:
            raise ValidationError('Дата окончания должна быть позже даты начала')

    def __init__(self, *args, **kwargs):
        super(AddScheduleSettingsForm, self).__init__(*args, **kwargs)
        self.direction_id.choices = [(d.id, d.name) for d in Direction.query.all()]

class EditScheduleSettingsForm(FlaskForm):
    settings_id = HiddenField('ID настроек')
    direction_id = SelectField('Направление', coerce=int, validators=[DataRequired()])
    start_date = DateField('Дата начала', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Дата окончания', format='%Y-%m-%d', validators=[DataRequired()])
    max_exams_per_day = IntegerField('Максимум экзаменов в день', validators=[
        DataRequired(),
        NumberRange(min=1, max=10, message="Допустимые значения 1-10")
    ])
    min_days_between_exams = IntegerField('Минимальный интервал между экзаменами', validators=[
        DataRequired(),
        NumberRange(min=1, max=10, message="Допустимые значения 1-10")
    ])
    submit = SubmitField('Сохранить изменения')

    def validate_end_date(self, field):
        if field.data < self.start_date.data:
            raise ValidationError('Дата окончания должна быть позже даты начала')

    def __init__(self, *args, **kwargs):
        super(EditScheduleSettingsForm, self).__init__(*args, **kwargs)
        self.direction_id.choices = [(d.id, d.name) for d in Direction.query.all()]

class AddTeacherForm(FlaskForm):
    first_name = StringField('Имя', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Length(max=50, message="Максимум 50 символов")
    ])
    last_name = StringField('Фамилия', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Length(max=50, message="Максимум 50 символов")
    ])
    patronymic = StringField('Отчество', validators=[
        Length(max=50, message="Максимум 50 символов"),
    ])
    email = StringField('Электронная почта', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Email(message="Некорректный формат email"),
        Length(max=120, message="Максимум 120 символов")
    ])
    submit = SubmitField('Добавить преподавателя')

    def validate_email(self, field):
        if Teacher.query.filter_by(email=field.data).first():
            raise ValidationError('Преподаватель с такой электронной почтой уже существует')


class EditTeacherForm(FlaskForm):
    teacher_id = HiddenField('ID преподавателя')
    first_name = StringField('Имя', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Length(max=50, message="Максимум 50 символов")
    ])
    last_name = StringField('Фамилия', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Length(max=50, message="Максимум 50 символов")
    ])
    patronymic = StringField('Отчество', validators=[
        Length(max=50, message="Максимум 50 символов")
    ])
    email = StringField('Электронная почта', validators=[
        DataRequired(message="Поле обязательно для заполнения"),
        Email(message="Некорректный формат email"),
        Length(max=120, message="Максимум 120 символов")
    ])
    submit = SubmitField('Сохранить изменения')

    def validate_email(self, field):
        teacher = Teacher.query.filter_by(email=field.data).first()
        # Добавляем проверку на наличие teacher_id.data
        if teacher and (self.teacher_id.data is None or teacher.id != int(self.teacher_id.data)):
            raise ValidationError('Преподаватель с такой электронной почтой уже существует')

class AddDirectionForm(FlaskForm):
    code = StringField('Код направления', validators=[
        DataRequired(),
        Length(max=20, message="Максимум 20 символов")
    ])
    name = StringField('Название направления', validators=[
        DataRequired(),
        Length(max=100, message="Максимум 100 символов")
    ])
    submit = SubmitField('Добавить направление')

    def validate_code(self, field):
        if Direction.query.filter_by(code=field.data).first():
            raise ValidationError('Направление с таким кодом уже существует')

class EditDirectionForm(FlaskForm):
    direction_id = HiddenField('ID направления')
    code = StringField('Код направления', validators=[
        DataRequired(),
        Length(max=20, message="Максимум 20 символов")
    ])
    name = StringField('Название направления', validators=[
        DataRequired(),
        Length(max=100, message="Максимум 100 символов")
    ])
    submit = SubmitField('Сохранить изменения')

    def validate_code(self, field):
        direction = Direction.query.filter_by(code=field.data).first()
        if direction and direction.id != int(self.direction_id.data):
            raise ValidationError('Направление с таким кодом уже существует')


# class GenerateScheduleForm(FlaskForm):
#     direction_id = SelectField('Направление', coerce=int, validators=[DataRequired()])
#     start_date = DateField('Начальная дата', validators=[DataRequired()])
#     end_date = DateField('Конечная дата', validators=[DataRequired()])
#     max_exams_per_day = IntegerField('Макс. экзаменов в день', validators=[DataRequired()])
#     min_days_between_exams = IntegerField('Минимальный интервал', validators=[DataRequired()])
#     submit = SubmitField('Сгенерировать')


class GenerateScheduleForm(FlaskForm):
    start_date = DateField('Дата начала', default=datetime.today)
    end_date = DateField('Дата окончания', default=datetime.today)
    max_exams_per_day = IntegerField('Макс. экзаменов в день', default=3)
    min_days_between_exams = IntegerField('Минимальный интервал (дни)', default=1)
    submit = SubmitField('Сгенерировать')

from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, SubmitField

class BackupForm(FlaskForm):
    csrf_token = HiddenField()  # Добавляем CSRF-токен

    file = FileField(
        'Файл резервной копии',
        validators=[
            FileRequired(message="Необходимо выбрать файл"),
            FileAllowed(
                ['sql', 'gz', 'dump'],  # Убрал 'backup' как нестандартное расширение
                message='Поддерживаются только SQL, GZIP и дампы PostgreSQL'
            )
        ],
        render_kw={
            'class': 'form-control-file',
            'accept': '.sql,.gz,.dump',
            'aria-describedby': 'fileHelp',
            'onchange': "showFileName(this)"
        }
    )

    submit = SubmitField(
        'Загрузить и восстановить',
        render_kw={
            'class': 'btn btn-warning btn-lg mt-3',
            'disabled': True  # Будет активирован после выбора файла
        }
    )

    def __init__(self, *args, **kwargs):
        super(BackupForm, self).__init__(*args, **kwargs)
        self.csrf_token.data = kwargs.get('csrf_token')

#
# class BackupForm(FlaskForm):
#     csrf_token = HiddenField()  # CSRF-токен
#
#     file = FileField(
#         'Файл резервной копии',
#         validators=[
#             FileRequired(message="Необходимо выбрать файл"),
#             FileAllowed(
#                 ['sql', 'gz', 'dump', 'sql.gz'],  # Поддерживаемые расширения
#                 message='Поддерживаются файлы SQL (plain/gzip) и дампы PostgreSQL'
#             )
#         ],
#         render_kw={
#             'class': 'custom-file-input',
#             'accept': '.sql,.sql.gz,.gz,.dump',
#             'aria-describedby': 'fileHelp',
#             'onchange': "updateFileName(this)",
#             'id': 'backupFile'
#         }
#     )
#
#     submit = SubmitField(
#         'Загрузить и восстановить',
#         render_kw={
#             'class': 'btn btn-primary btn-lg mt-3',
#             'disabled': True,
#             'id': 'submitBtn'
#         }
#     )
#
#     backup_type = RadioField(
#         'Тип резервной копии',
#         choices=[
#             ('auto', 'Автоматическое определение'),
#             ('postgresql', 'PostgreSQL дамп'),
#             ('mysql', 'MySQL дамп')
#         ],
#         default='auto',
#         render_kw={
#             'class': 'form-check-input',
#             'id': 'backupType'
#         }
#     )
#
#     def __init__(self, *args, **kwargs):
#         super(BackupForm, self).__init__(*args, **kwargs)
#         self.csrf_token.data = kwargs.get('csrf_token')