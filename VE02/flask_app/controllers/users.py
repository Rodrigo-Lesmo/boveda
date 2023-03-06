from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import Usuario
from flask_app.models.deposito import Deposito
from flask_app.models.ubicacion import Ubicacion
from flask_app.models.entrada import Entrada
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def log():
    return render_template("login.html")


@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("index.html", usuario=Usuario.get_by_id(data), ubicacion=Ubicacion.get_by_name(),
                           entra=Entrada.get_by_name())


@app.route('/deposito')
def deposito():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("deposito.html", depositos=Deposito.get_by_name(), usuario=Usuario.get_by_id(data))


@app.route('/ubicacion')
def ubicacion():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("ubicacion.html", ubicaciones=Ubicacion.get_by_name(), depositos=Deposito.get_by_name(), usuario=Usuario.get_by_id(data))


@app.route('/usuarios')
def usuarios():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template("usuarios.html", usu=Usuario.get_all(), usuario=Usuario.get_by_id(data))


@app.route('/regusuario', methods=['POST'])
def regi_usuario():
    if not Usuario.validate_register(request.form):
        return redirect('/usuarios')
    else:
        data = {
            "nombres": request.form['nombres'],
            "apellidos": request.form['apellidos'],
            "cedula": request.form['cedula'],
            "contrasena": bcrypt.generate_password_hash(request.form['contrasena']),
            "correo": request.form['correo'],
            "nivel": request.form['nivel'],
            "estado": request.form['estado'],
        }
    Usuario.save(data)

    return redirect('/usuarios')


@app.route('/update/usuario', methods=['POST'])
def update_usuario():
    data = {
        "nombres": request.form['nombres'],
        "apellidos": request.form['apellidos'],
        "cedula": request.form['cedula'],
        "contrasena": bcrypt.generate_password_hash(request.form['contrasena']),
        "correo": request.form['correo'],
        "nivel": request.form['nivel'],
        "estado": request.form['estado'],
        "id_usuario": request.form['id_usuario'],
    }
    Usuario.update(data)
    return redirect('/usuarios')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if (request.form.get('correo') == '') or (request.form.get('contrasena') == ''):
        flash("Complete the fields!", "login")
        return redirect('/')
    else:
        data = {
            'correo': request.form.get('correo')
        }
        user = Usuario.get_by_email(data)
        if not user:
            flash("Invalid Email", "login")
            return redirect('/')
        if not bcrypt.check_password_hash(user.contrasena, request.form['contrasena']):
            flash("Invalid Password", "login")
            return redirect('/')
        session['user_id'] = user.id_usuario
    return redirect('/index')


@app.route('/delete/<int:id_usuario>')
def del_usuario(id_usuario):
    data = {
        'id_usuario': id_usuario,
    }
    Usuario.destroy(data)
    return redirect('/usuarios')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
