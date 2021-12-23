import os
import secrets
from datetime import datetime
from PIL import Image #dá resize nos icons para nao ocupar muito espaço
from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from projeto import app, db, bcrypt
from projeto.forms import Registo, Login, UpdateConta, nova_Aposta
from projeto.models import User, Aposta, Evento
from flask_login import login_user, current_user, logout_user, login_required
import json

data = json.load(open("C:/Users/beatr/Desktop/RASproj/Api.json"))

@app.route("/")
@app.route("/home")
def home():
    #usa template
    return render_template('home.html', data=data)

@app.route("/about")
def about():
    return render_template('about.html', title='Sobre a Aplicação')

@app.route("/registo", methods=['GET','POST'])
def registo():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Registo()
    req = request.form

    idade = req.get('idade')
    username = req.get('username')
    email = req.get('email')

    if 0 < int(-1 if idade is None else idade)  < 17:
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
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, saldoEuro=0, saldoLibra=0, saldoDollar=0, saldoCardan=0)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
    return render_template('registo.html', title='Registo',form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            #Se tentar aceder a /conta sem ter login, pede para fazer login e leva para a route que queria inicialmente
            next_page = request.args.get('next') 
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login sem sucesso','danger')
    return render_template('login.html', title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def guarda_foto(form_foto):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_foto.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/fotosDePerfil', picture_fn)
    output_size = (125,125)
    i = Image.open(form_foto)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/conta", methods=['GET', 'POST'])
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
        return redirect(url_for('conta'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.DepositoEuro.data = 0
        form.DepositoDollar.data = 0
        form.DepositoLibra.data = 0
        form.DepositoCardan.data = 0
    image_file = url_for('static', filename='fotosDePerfil/' + current_user.image_file)
    return render_template('conta.html', title='A minha Conta',form=form, image_file=image_file)


@app.route("/aposta/nova", methods=['GET', 'POST'])
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
        return redirect(url_for('home'))
    
    return render_template('novaAposta.html', title='Nova Aposta', form=form)

@app.route("/aposta/<desporto>", methods=['GET', 'POST'])
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
                    if p.dia == currentDay:
                        if p.hora < currentHour:
                            flash('Houve atualização de apostas, Jogo de {p.equipa} terminou!','success')
                            p.estado = 'Fechado'
                        if p.hora == currentHour:
                            if currentMinute >= p.minuto:
                                flash('Houve atualização de apostas','success')
                                p.estado = 'Fechado'
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


@app.route("/mybets", methods=['GET', 'POST'])
@login_required 
def myapostas():
    atualizaApostas()
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    apostas = Aposta.query.filter_by(user_id=user.id)\
               .order_by(Aposta.mes.desc())\
               .paginate(page=page, per_page=10)

    
    return render_template('apostas.html', apostas=apostas,user=user)

    



    
