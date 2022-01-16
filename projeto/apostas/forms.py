from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Email, ValidationError
from projeto.models import User 

class nova_Aposta(FlaskForm):
    desporto = SelectField('Desporto', choices=[('Tenis','Tenis'),('Futebol','Futebol')], validators=[DataRequired()])
    moeda = SelectField('Moeda',choices=[('€','Euro'),('£','Libra'),('$','Dollar'),('C','Cardan')],validators=[DataRequired()])
    valor = IntegerField('Valor', validators=[DataRequired(), NumberRange(min=0)])
    evento = SelectField('Evento', choices=[], validators = [DataRequired()])

    submit = SubmitField('Fazer Aposta')

class cambio_moedas(FlaskForm):
    moeda = SelectField('Moeda',choices=[('€','Euro')],validators=[DataRequired()])
    moeda2 = SelectField('Moeda2', choices=[('C','Cardan')],validators=[DataRequired()])
    valor = IntegerField('Valor', validators=[DataRequired(), NumberRange(min=0)])

    submit = SubmitField('Cambiar')


