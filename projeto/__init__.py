#Inicializa aplicação
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rasfase2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message = 'info'

#from projeto import routes
from projeto.users.routes import users
from projeto.apostas.routes import apostas
from projeto.main.routes import main

app.register_blueprint(users)
app.register_blueprint(apostas)
app.register_blueprint(main)


