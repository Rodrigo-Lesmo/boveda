from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.deposito import Deposito


@app.route('/regdeposito', methods=['POST'])
def register():
    data = {
        "descripcion": request.form['descripcion'],
        "id_usuario": session['user_id']
    }
    Deposito.save(data)
    return redirect('/deposito')


@app.route('/update/deposito', methods=['POST'])
def update_deposito():
    data = {
        "descripcion": request.form["descripcion"],
        "id_deposito": request.form['id_deposito']
    }
    Deposito.update(data)
    return redirect('/deposito')


@app.route('/dele/<int:id_deposito>')
def dele(id_deposito):
    data = {
        'id_deposito': id_deposito,
    }
    Deposito.destroy(data)
    return redirect('/deposito')
