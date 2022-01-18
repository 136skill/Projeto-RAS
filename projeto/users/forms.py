from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Email, ValidationError
from projeto.models import User 

class Registo(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmar_password = PasswordField('Confirmar Password', validators=[DataRequired(), EqualTo('password')])
    idade = StringField('Idade', validators=[DataRequired()])
    estado = SelectField('Tipo de Conta', choices= [('1','Normal'),('2','Premium')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class Login(FlaskForm):
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateConta(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    foto = FileField('Atualizar Foto', validators=[FileAllowed(['jpg','png'])])
    DepositoEuro = IntegerField('Depósito (Euro)', validators = [NumberRange(min=0)])
    DepositoDollar = IntegerField('Depósito (Dollar)', validators = [NumberRange(min=0)])
    DepositoLibra = IntegerField('Depósito (Libra)', validators = [NumberRange(min=0)])
    DepositoCardan = IntegerField('Depósito (Cardan)', validators = [NumberRange(min=0)])

    submit = SubmitField('Atualizar Dados')

class cash_out(FlaskForm):
    moeda = SelectField('Moeda',choices=[('€','Euro'),('£','Libra'),('$','Dollar'),('C','Cardan')],validators=[DataRequired()])
    valor = IntegerField('Valor', validators=[DataRequired(), NumberRange(min=0)])

    submit = SubmitField('Cash Out')

class Questionario(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Enviar')
