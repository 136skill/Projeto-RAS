from flask import Blueprint
import os
import secrets
from datetime import datetime
from PIL import Image #dá resize nos icons para nao ocupar muito espaço
from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from projeto import app, db, bcrypt
from projeto.apostas.forms import nova_Aposta, cambio_moedas
from projeto.models import User, Aposta, Evento, Taxa
from flask_login import login_user, current_user, logout_user, login_required
import json

apostas = Blueprint('apostas',__name__)

@apostas.route("/aposta/nova", methods=['GET', 'POST'])
@login_required
def novaAposta():
    atualizaApostas()
    form = nova_Aposta()
    req = request.form
    valor = req.get('valor')
    moeda = req.get('moeda')

    if form.moeda.data == '€':
        if current_user.saldoEuro < int(0 if valor is None else valor):
            flash('Não tem saldo suficiente!','danger')
            return render_template('novaAposta.html', title='Nova Aposta', form=form)

    if form.moeda.data == '$':
        if current_user.saldoDollar < int(0 if valor is None else valor):
            flash('Não tem saldo suficiente!','danger')
            return render_template('novaAposta.html', title='Nova Aposta', form=form)

    if form.moeda.data == '£':
        if current_user.saldoLibra < int(0 if valor is None else valor):
            flash('Não tem saldo suficiente!','danger')
            return render_template('novaAposta.html', title='Nova Aposta', form=form)

    if form.moeda.data == 'C':
        if current_user.saldoCardan < int(0 if valor is None else valor):
            flash('Não tem saldo suficiente!','danger')
            return render_template('novaAposta.html', title='Nova Aposta', form=form)
    
    
    form.evento.choices = [(evento.id, 'Jogo:' + str(evento.liga) + '\n Equipa:' + str(evento.equipa) + '\n Odd:' + str(evento.odd)) for evento in Evento.query.filter_by(desporto='Tenis').all()]

    if request.method == 'POST':
        evento = Evento.query.filter_by(id=form.evento.data).first()
        useratS = User.query.filter_by(id=current_user.id).first()
        if form.moeda.data == '€':
            current_user.saldoEuro = (useratS.saldoEuro - int(form.valor.data))
        if form.moeda.data == '£':
            current_user.saldoLibra = (useratS.saldoLibra - int(form.valor.data))
        if form.moeda.data == '$':
            current_user.saldoDollar = (useratS.saldoDollar - int(form.valor.data))
        if form.moeda.data == 'C':
            current_user.saldoCardan = (useratS.saldoCardan - int(form.valor.data))
        nova = Aposta(desporto=form.desporto.data, dia=evento.dia, mes=evento.mes,ano=evento.ano,hora=evento.hora,minuto=evento.minuto,evento=evento.liga, estado="Aberto",equipa=evento.equipa,valor=form.valor.data,moeda=form.moeda.data,odd=evento.odd,potencial=evento.potencial,user_id=current_user.id)
        db.session.add(nova)
        db.session.commit()
        flash('Aposta efetuada com sucesso!','success')
        return redirect(url_for('main.home'))
    
    return render_template('novaAposta.html', title='Nova Aposta', form=form)

@apostas.route("/aposta/<desporto>", methods=['GET', 'POST'])
@login_required 
def evento(desporto):
    eventos = Evento.query.filter_by(desporto=desporto).all()
    eventoARR = []
    for evento in eventos:
        eventoObj={}
        eventoObj['id'] = evento.id
        eventoObj['liga'] = evento.liga
        eventoObj['equipa'] = evento.equipa
        eventoObj['odd'] = evento.odd
        eventoARR.append(eventoObj)

    return jsonify({'eventos' : eventoARR })


def atualizaApostas():
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    currentHour = datetime.now().hour
    currentMinute = datetime.now().minute

    aposta = Aposta.query.filter_by(user_id=current_user.id).all()
    for p in aposta:
        if p.estado == 'Aberto':
            if p.ano <= currentYear:
                if p.mes <= currentMonth:
                    if p.dia < currentDay:
                        flash('Houve atualização de apostas','success')
                        p.estado = 'Fechado'
                        atualizaSaldo(p)
                    if p.dia == currentDay:
                        if p.hora < currentHour:
                            flash('Houve atualização de apostas, Jogo de {p.equipa} terminou!','success')
                            p.estado = 'Fechado'
                            atualizaSaldo(p)
                        if p.hora == currentHour:
                            if currentMinute > p.minuto:
                                flash('Houve atualização de apostas','success')
                                p.estado = 'Fechado'
                                atualizaSaldo(p)
    db.session.commit()
                    
def atualizaSaldo(p):         
    if(p.potencial=='G'):
        if (p.moeda == '€'):
            usernow = User.query.filter_by(username=current_user.username).first()
            current_user.saldoEuro += (p.valor * p.odd)
        if (p.moeda == '$'):
            usernow = User.query.filter_by(username=current_user.username).first()
            current_user.saldoDollar += (p.valor * p.odd)
        if (p.moeda == '£'):
            usernow = User.query.filter_by(username=current_user.username).first()
            current_user.saldoLibra += (p.valor * p.odd)
        if (p.moeda == 'C'):
            usernow = User.query.filter_by(username=current_user.username).first()
            current_user.saldoCardan += (p.valor * p.odd)
    else:
        if(p.moeda == '€'):
            usernow = User.query.filter_by(username=current_user.username).first()
            current_user.saldoEuro -= (p.valor * p.odd)
        if(p.moeda == '$'):
            usernow = User.query.filter_by(username=current_user.username).first()
            current_user.saldoDollar -= (p.valor * p.odd)
        if(p.moeda == '£'):
            usernow = User.query.filter_by(username=current_user.username).first()
            current_user.saldoLibra -= (p.valor * p.odd)
        if(p.moeda == 'C'):
            usernow = User.query.filter_by(username=current_user.username).first()
            current_user.saldoCardan -= (p.valor * p.odd)   

    db.session.commit()


@apostas.route("/cambio", methods=['GET', 'POST'])
@login_required 
def cambio():
    atualizaApostas()

    form = cambio_moedas()
    req = request.form
    valor = req.get('valor')

    if form.validate_on_submit():
        if form.moeda.data == '€' and form.moeda2.data == 'C':
            if current_user.saldoEuro < form.valor.data:
                flash('Não tem saldo suficiente','danger')
            else: 
                tax = Taxa.query.filter_by(id=1).first()
                current_user.saldoEuro -= int(valor)
                current_user.saldoCardan += int(valor)*int(tax.taxas)
                flash('Câmbio realizado com sucesso','success')
    

    db.session.commit()
    return render_template('cambio.html', form=form)


        # if form.moeda.data == '€' and form.moeda2.data = '£':
        
        # if form.moeda.data == '€' and form.moeda2.data = '$':

        # if form.moeda.data == 'C' and form.moeda2.data = '$':

        # if form.moeda.data == 'C' and form.moeda2.data = '£':

        # if form.moeda.data == 'C' and form.moeda2.data = '€':

        # if form.moeda.data == '£' and form.moeda2.data = '€':
        
        # if form.moeda.data == '£' and form.moeda2.data = 'C':
        
        # if form.moeda.data == '£' and form.moeda2.data = '$':

        # if form.moeda.data == '$' and form.moeda2.data = 'C':

        # if form.moeda.data == '$' and form.moeda2.data = '£':

        # if form.moeda.data == '$' and form.moeda2.data = '€':
