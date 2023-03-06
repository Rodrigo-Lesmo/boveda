from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.ubicacion import Ubicacion


@app.route('/regubicacion', methods=['POST'])
def regubicacion():
    data = {
        "descripcion": request.form['descripcion'],
        "estado": request.form['estado'],
        "id_usuario": session['user_id'],
        "id_deposito": request.form['id_deposito']
    }
    Ubicacion.save(data)
    return redirect('/ubicacion')


@app.route('/update/ubicacion', methods=['POST'])
def update_ubicacion():
    data = {
        "id_ubicacion": request.form['id_ubicacion'],
        "descripcion": request.form['descripcion'],
        "estado": request.form['estado'],
        "id_deposito": request.form['id_deposito']
    }
    Ubicacion.update(data)
    return redirect('/ubicacion')


@app.route('/del/<int:id_ubicacion>')
def dele_ubi(id_ubicacion):
    data = {
        'id_ubicacion': id_ubicacion,
    }
    Ubicacion.destroy(data)
    return redirect('/ubicacion')
