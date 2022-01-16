from flask import Blueprint
import os
import secrets
from datetime import datetime
from PIL import Image #dá resize nos icons para nao ocupar muito espaço
from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from projeto import app, db, bcrypt
from projeto.models import User, Aposta, Evento, Taxa
from flask_login import login_user, current_user, logout_user, login_required
import json

main = Blueprint('main',__name__)


data = json.load(open("C:/Users/beatr/Desktop/RASCodigo/Api.json"))
camb = json.load(open("C:/Users/beatr/Desktop/RASCodigo/Cambio.json"))

def loadEventos():
    t = True
    x = True
    for evento in data['Eventos']:
        ev = Evento.query.filter_by(id=evento['id']).first()
       
        if ev and t:
            t = False
            flash('Eventos desportivos up to date!', 'success')
        if not ev:
            novo = Evento(id=evento['id'], desporto=evento['Desporto'], equipa=evento['Atleta'], liga=evento['Liga'],jornada=evento['Jornada'], odd=evento['Odd'], dia=evento['Dia'], mes=evento['Mes'],ano=evento['Ano'],hora=evento['Hora'],minuto=evento['Minuto'],potencial=evento['Potencial'])
            db.session.add(novo)
            db.session.commit()
            if x:
                flash('Novos eventos desportivos disponíveis!', 'success')
                x = False


def loadTaxa():
    t = True
    for taxas in camb['Taxas']:
        cb = Taxa.query.filter_by(id=taxas['id']).first()

        if not cb :
            taxa = Taxa(id=taxas['id'], moeda = taxas['Moeda'], moeda2 = taxas['Moeda2'], taxas = float(taxas['taxa']))
            db.session.add(taxa)
            flash('Taxas diárias de câmbio atualizadas','success')

        if cb and cb.taxas != taxas['taxa']:
            cb.taxas = float(taxas['taxa'])
            if t:
                flash('Taxas diárias de câmbio atualizadas','success')
                t=False

        if cb and cb.taxas == taxas['taxa']:
            if t:
                flash('Taxas diárias prontas','success')
                t=False

        db.session.commit()



@main.route("/")
@main.route("/home")
def home():
    #usa template
    loadEventos()
    loadTaxa()
    return render_template('home.html', data=data)

@main.route("/about")
def about():
    return render_template('about.html', title='Sobre a Aplicação')
