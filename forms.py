from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Сохранить данные')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    """Форма регистрации"""
    user_name = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email адрес', validators=[DataRequired(), Email()])
    password_hash = PasswordField('Пароль', validators=[DataRequired()])
    confirm = PasswordField('Повторите пароль', validators=[DataRequired()])
    accept_tos = BooleanField('Я принимаю лицензионное соглашение и условия пользования',
                              validators=[DataRequired()])
    submit = SubmitField('Создать учетную запись')


class AddDoll(FlaskForm):
    price = IntegerField('Цена', validators=[DataRequired()])
    color_of_hair = IntegerField('Цвет волос', validators=[DataRequired()])
    rarity = StringField('Уникальность', validators=[DataRequired()])
    dealer_id = SelectField('Номер поставщика', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить куклу в коллецию')


class AddDealerForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Добавить поставщика')


class SearchPriceForm(FlaskForm):
    start_price = IntegerField('Минимальная цена', validators=[DataRequired()], default=500000)
    end_price = IntegerField('Максимальная цена', validators=[DataRequired()], default=1000000)
    submit = SubmitField('Поиск')


class SearchDealerForm(FlaskForm):
    dealer_id = SelectField('Номер поставщика', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Поиск')