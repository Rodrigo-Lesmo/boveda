from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import Usuario
from flask_app.models.deposito import Deposito
from flask_app.models.ubicacion import Ubicacion
from flask_app.models.entrada import Entrada


@app.route('/regentrada', methods=['POST'])
def reg_entrada():
    data = {
        "referencia": request.form['referencia'],
        "caratula": request.form['caratula'],
        "instrumento": request.form['instrumento'],
        "tipo": request.form['tipo'],
        "estado": request.form['estado'],
        "observacion": request.form['observacion'],
        "nro_oficio": request.form['nro_oficio'],
        "id_usuario": session['user_id'],
        "id_ubicacion": request.form['id_ubicacion']
    }
    Entrada.save(data)

    return redirect('/index')


@app.route('/desactivate/<int:id_entrada>')
def des_entrada(id_entrada):
    data = {
        'id_entrada': id_entrada,
    }
    Entrada.desactivate(data)
    return redirect('/index')


@app.route('/update/entrada', methods=['POST'])
def update_entrada():
    data = {
        "referencia": request.form['referencia'],
        "caratula": request.form['caratula'],
        "instrumento": request.form['instrumento'],
        "tipo": request.form['tipo'],
        "observacion": request.form['observacion'],
        "nro_oficio": request.form['nro_oficio'],
        "id_ubicacion": request.form['id_ubicacion'],
        "id_entrada": request.form['id_entrada']
    }
    Entrada.update(data)
    return redirect('/index')
