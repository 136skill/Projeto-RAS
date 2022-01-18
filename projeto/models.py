from datetime import datetime
from projeto import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.Integer, unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    saldoEuro = db.Column(db.Integer, nullable=False)
    saldoLibra = db.Column(db.Integer, nullable=False)
    saldoDollar = db.Column(db.Integer, nullable=False)
    saldoCardan = db.Column(db.Integer, nullable=False)
    apostas = db.relationship('Aposta', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.saldoEuro}')"


class Aposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desporto = db.Column(db.String(100), nullable=False)
    dia = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    hora = db.Column(db.Integer, nullable=False)
    minuto = db.Column(db.Integer, nullable=False)
    evento = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    equipa = db.Column(db.String(20), nullable=False)
    valor = db.Column(db.Integer, nullable=False)
    moeda = db.Column(db.String(20),nullable=False)
    odd = db.Column(db.Integer, nullable=False)
    potencial = db.Column(db.String(5),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    
    def __repr__(self):
        return f"Aposta('{self.desporto}', '{self.id}', '{self.user_id}')"

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desporto = db.Column(db.String(20),nullable=False)
    equipa = db.Column(db.String(20),nullable=False)
    liga = db.Column(db.String(20),nullable=False)
    jornada = db.Column(db.String(20),nullable=False)
    odd = db.Column(db.Integer, nullable=False)
    dia = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    hora = db.Column(db.Integer, nullable=False)
    minuto = db.Column(db.Integer,nullable=False)
    potencial = db.Column(db.String(5),nullable=False)

    def __repr__(self):
        return f"Evento('{self.desporto}', '{self.equipa}', '{self.odd}', '{self.liga}')"

class Taxa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    moeda = db.Column(db.String(20),nullable=False)
    moeda2 = db.Column(db.String(20),nullable=False)
    taxas = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"Taxas('{self.moeda}', '{self.moeda2}', '{self.taxas}')"

