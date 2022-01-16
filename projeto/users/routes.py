from flask import Blueprint
import os
import secrets
from datetime import datetime
from PIL import Image #dá resize nos icons para nao ocupar muito espaço
from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from projeto import app, db, bcrypt
from projeto.users.forms import Registo, Login, UpdateConta, cash_out
from projeto.users.utils import guarda_foto
from projeto.models import User, Aposta, Evento, Taxa
from flask_login import login_user, current_user, logout_user, login_required
import json
from projeto.apostas.routes import atualizaApostas, atualizaSaldo

users = Blueprint('users',__name__)

@users.route("/registo", methods=['GET','POST'])
def registo():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = Registo()
    req = request.form

    idade = req.get('idade')
    username = req.get('username')
    email = req.get('email')
    

    if 0 < int(-1 if idade is None else idade)  < 18:
        flash('Não é maior de idade!', 'danger')
        return render_template('registo.html', title='Registo',form=form)

    if form.validate_on_submit():
        
        user = User.query.filter_by(username=username).first()
        email1 =  User.query.filter_by(username=email).first()

        if user:
            flash('Este username já existe', 'danger')
            return render_template('registo.html', title='Registo',form=form)
        if email1:
            flash('Já existe uma conta registada com este email', 'danger')
            return render_template('registo.html', title='Registo',form=form)
        else:
            #if form.data.estado == '1':
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, saldoEuro=0, saldoLibra=0, saldoDollar=0, saldoCardan=0)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('users.login'))
            #else:
            #   hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            #   user = User(estado = 2, username=form.username.data, email=form.email.data, password=hashed_password, saldoEuro=0, saldoLibra=0, saldoDollar=0, saldoCardan=0)
            #   db.session.add(user)
            #   db.session.commit()
            #   flash(f'Account created for {form.username.data}!', 'success')
            #   return redirect(url_for('login'))
     

    return render_template('registo.html', title='Registo',form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            #Se tentar aceder a /conta sem ter login, pede para fazer login e leva para a route que queria inicialmente
            next_page = request.args.get('next') 
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login sem sucesso','danger')
    return render_template('login.html', title='Login',form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/conta", methods=['GET', 'POST'])
@login_required
def conta():
    form = UpdateConta() 
    req = request.form
    username = req.get('username')
    email = req.get('email')
    DE = req.get('DepositoEuro')
    DD = req.get('DepositoDollar')
    DC = req.get('DepositoCardan')
    DL = req.get('DepositoLibra')

    atualizaApostas()
    if form.validate_on_submit():
        if form.foto.data:
            picture_file = guarda_foto(form.foto.data)
            current_user.image_file = picture_file

        if username != current_user.username:
            user = User.query.filter_by(username=username).first()
            if user:
                flash('Já existe um utilizador com este username', 'danger')
                return render_template('conta.html', title='A minha conta',form=form)
            else:
                current_user.username = form.username.data
                
        if email != current_user.email:
            email1 =  User.query.filter_by(username=email).first()
            if email1:
                flash('Já existe uma conta com este email registado','danger')
                return render_template('conta.html', title='A minha conta', form=form)
            else:
                current_user.email = form.email.data

        if(DD != 0):
            if 1 < int(DD) < 5:
                flash('O depósito deve ser superior a 5$','danger')
                return render_template('conta.html', title='A minha conta', form=form)
            else:
                userat = User.query.filter_by(username=username).first()
                current_user.saldoDollar = (form.DepositoDollar.data + int(userat.saldoDollar))
        if(DD == 0):
            current_user.saldoDollar = current_user.saldoDollar

        if(DE != 0):
            if 1 < int(DE) < 5:
                flash('O depósito deve ser superior a 5€','danger')
                return render_template('conta.html', title='A minha conta', form=form)
            else:
                userat = User.query.filter_by(username=username).first()
                current_user.saldoEuro = (form.DepositoEuro.data + int(userat.saldoEuro))
        if(DE == 0):
            current_user.saldoEuro = current_user.saldoEuro

        if(DL != 0):
            if 1 < int(DL) < 5:
                flash('O depósito deve ser superior a 5£','danger')
                return render_template('conta.html', title='A minha conta', form=form)
            else:
                userat = User.query.filter_by(username=username).first()
                current_user.saldoLibra = (form.DepositoLibra.data + int(userat.saldoLibra))
        if(DL == 0):
            current_user.saldoLibra = current_user.saldoLibra

        if(DC != 0):
            if 1 < int(DC) < 5:
                flash('O depósito deve ser superior a 5C','danger')
                return render_template('conta.html', title='A minha conta', form=form)
            else:
                userat = User.query.filter_by(username=username).first()
                current_user.saldoCardan = (form.DepositoCardan.data + int(userat.saldoCardan))
        if(DC == 0):
            current_user.saldoCardan = current_user.saldoCardan
        
        db.session.commit()
        flash('Conta atualizado com sucesso!','success')
        return redirect(url_for('users.conta'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.DepositoEuro.data = 0
        form.DepositoDollar.data = 0
        form.DepositoLibra.data = 0
        form.DepositoCardan.data = 0
    image_file = url_for('static', filename='fotosDePerfil/' + current_user.image_file)
    return render_template('conta.html', title='A minha Conta',form=form, image_file=image_file)


@users.route("/mybets", methods=['GET', 'POST'])
@login_required 
def myapostas():
    atualizaApostas()
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    apostas = Aposta.query.filter_by(user_id=user.id)\
               .order_by(Aposta.mes.desc())\
               .paginate(page=page, per_page=10)
    
    return render_template('apostas.html', apostas=apostas,user=user)

@users.route("/cashout", methods=['GET', 'POST'])
@login_required 
def cashout():
    form = cash_out() 
    req = request.form
    moeda = req.get('moeda')
    valor = req.get('valor')

    atualizaApostas()

    if form.validate_on_submit():
        if form.moeda.data == '€':
            if current_user.saldoEuro < int(0 if valor is None else valor):
                flash('Não tem saldo suficiente!','danger')
                return render_template('cashout.html', title='Cash Out', form=form)
            else:
                usernow = User.query.filter_by(username=current_user.username).first()
                flash('Transferência bem sucedida','success')
                current_user.saldoEuro = usernow.saldoEuro - int(valor)


        if form.moeda.data == '$':
            if current_user.saldoDollar < int(0 if valor is None else valor):
                flash('Não tem saldo suficiente!','danger')
                return render_template('cashout.html', title='Cash Out', form=form)
            else:
                usernow = User.query.filter_by(username=current_user.username).first()
                flash('Transferência bem sucedida','success')
                current_user.saldoDollar -= int(valor)

        if form.moeda.data == '£':
            if current_user.saldoLibra < int(0 if valor is None else valor):
                flash('Não tem saldo suficiente!','danger')
                return render_template('cashout.html', title='Cash Out', form=form)
            else:
                usernow = User.query.filter_by(username=current_user.username).first()
                flash('Transferência bem sucedida','success')
                current_user.saldoLibra -= int(valor)

        if form.moeda.data == 'C':
            if current_user.saldoCardan < int(0 if valor is None else valor):
                flash('Não tem saldo suficiente!','danger')
                return render_template('cashout.html', title='Cash Out', form=form)
            else:
                usernow = User.query.filter_by(username=current_user.username).first()
                flash('Transferência bem sucedida','success')
                current_user.saldoCardan -= int(valor)
    
    db.session.commit()

    return render_template('cashout.html', form=form)
