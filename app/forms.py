from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, HiddenField, DateField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, NumberRange
from app.models.user import User

from app.models.models import Direction, Specialization, StudentGroup, Subject, Teacher, Room
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

class AddSubjectForm(FlaskForm):
    name = StringField('Название предмета', validators=[
        DataRequired(),
        Length(max=100, message="Максимум 100 символов")
    ])
    submit = SubmitField('Добавить предмет')

    def validate_name(self, field):
        if Subject.query.filter_by(name=field.data).first():
            raise ValidationError('Предмет с таким названием уже существует')

class EditSubjectForm(FlaskForm):
    subject_id = HiddenField('ID предмета')
    name = StringField('Название предмета', validators=[
        DataRequired(),
        Length(max=100, message="Максимум 100 символов")
    ])
    submit = SubmitField('Сохранить изменения')

    def validate_name(self, field):
        subject = Subject.query.filter_by(name=field.data).first()
        if subject and subject.id != int(self.subject_id.data):
            raise ValidationError('Предмет с таким названием уже существует')

### 3. Формы для группы (StudentGroup) ###
class AddGroupForm(FlaskForm):
    name = StringField('Название группы', validators=[
        DataRequired(),
        Length(max=50, message="Максимум 50 символов")
    ])
    specialization_id = SelectField('Специальность', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить группу')

    def __init__(self, *args, **kwargs):
        super(AddGroupForm, self).__init__(*args, **kwargs)
        self.specialization_id.choices = [(s.id, s.name) for s in Specialization.query.all()]

    def validate_name(self, field):
        if StudentGroup.query.filter_by(name=field.data).first():
            raise ValidationError('Группа с таким названием уже существует')


class EditGroupForm(FlaskForm):
    group_id = HiddenField('ID группы')
    name = StringField('Название группы', validators=[
        DataRequired(),
        Length(max=50, message="Максимум 50 символов")
    ])
    specialization_id = SelectField('Специальность', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения')

    def __init__(self, *args, **kwargs):
        super(EditGroupForm, self).__init__(*args, **kwargs)
        self.specialization_id.choices = [(s.id, s.name) for s in Specialization.query.all()]

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
    submit = SubmitField('Добавить аудиторию')

    def validate_number(self, field):
        if Room.query.filter_by(number=field.data).first():
            raise ValidationError('Аудитория с таким номером уже существует')

class EditRoomForm(FlaskForm):
    room_id = HiddenField('ID аудитории')
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
    submit = SubmitField('Сохранить изменения')

    def validate_number(self, field):
        room = Room.query.filter_by(number=field.data).first()
        if room and room.id != int(self.room_id.data):
            raise ValidationError('Аудитория с таким номером уже существует')

### 5. Формы для экзамена (Exam) ###
class AddExamForm(FlaskForm):
    datetime = DateTimeField('Дата и время', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
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
        self.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
        self.group_id.choices = [(g.id, g.name) for g in StudentGroup.query.all()]
        self.teacher_id.choices = [(t.id, t.name) for t in Teacher.query.all()]
        self.room_id.choices = [(r.id, r.number) for r in Room.query.all()]

class EditExamForm(FlaskForm):
    exam_id = HiddenField('ID экзамена')
    datetime = DateTimeField('Дата и время', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
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
        super(EditExamForm, self).__init__(*args, **kwargs)
        self.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
        self.group_id.choices = [(g.id, g.name) for g in StudentGroup.query.all()]
        self.teacher_id.choices = [(t.id, t.name) for t in Teacher.query.all()]
        self.room_id.choices = [(r.id, r.number) for r in Room.query.all()]

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
    name = StringField('ФИО преподавателя', validators=[
        DataRequired(),
        Length(max=100, message="Максимум 100 символов")
    ])
    submit = SubmitField('Добавить преподавателя')

    def validate_name(self, field):
        if Teacher.query.filter_by(name=field.data).first():
            raise ValidationError('Преподаватель с таким именем уже существует')

class EditTeacherForm(FlaskForm):
    teacher_id = HiddenField('ID преподавателя')
    name = StringField('ФИО преподавателя', validators=[
        DataRequired(),
        Length(max=100, message="Максимум 100 символов")
    ])
    submit = SubmitField('Сохранить изменения')

    def validate_name(self, field):
        teacher = Teacher.query.filter_by(name=field.data).first()
        if teacher and teacher.id != int(self.teacher_id.data):
            raise ValidationError('Преподаватель с таким именем уже существует')


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