import os
import secrets
from datetime import datetime
from PIL import Image #dá resize nos icons para nao ocupar muito espaço
from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from projeto import app, db, bcrypt
from projeto.models import User, Aposta, Evento, Taxa
from flask_login import login_user, current_user, logout_user, login_required
import json


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