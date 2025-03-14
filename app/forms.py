from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from app.models.user import User

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
