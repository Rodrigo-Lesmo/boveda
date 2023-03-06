from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class Usuario:
    db_name = "boveda"

    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nombres = data['nombres']
        self.apellidos = data['apellidos']
        self.cedula = data['cedula']
        self.contrasena = data['contrasena']
        self.correo = data['correo']
        self.nivel = data['nivel']
        self.estado = data['estado']
        self.creado_en = data['creado_en']
        self.actualizado_en = data['actualizado_en']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuario (nombres,apellidos,cedula,contrasena,correo,nivel,estado,creado_en,actualizado_en) VALUES (%(nombres)s," \
                "%(apellidos)s,%(cedula)s,%(contrasena)s,%(correo)s,%(nivel)s,%(estado)s,now(),now())"
        print(query)
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuario;"
        users_from_db = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for u in users_from_db:
            users.append(cls(u))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM usuario WHERE correo = %(correo)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM usuario WHERE id_usuario = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE usuario SET nombres=%(nombres)s, apellidos=%(apellidos)s, cedula=%(cedula)s, " \
                "contrasena=%(contrasena)s, correo=%(correo)s, nivel=%(nivel)s, estado=%(estado)s, " \
                "actualizado_en=now() WHERE id_usuario = %(id_usuario)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM usuario WHERE id_usuario = %(id_usuario)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM usuario WHERE correo = %(correo)s;"
        results = connectToMySQL(Usuario.db_name).query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['correo']):
            flash("Invalid Email!!!", "register")
            is_valid = False
        if len(user['nombres']) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(user['apellidos']) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if len(user['contrasena']) < 4:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['contrasena'] != user['confirmar']:
            flash("Passwords don't match", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        query = "SELECT * FROM usuario WHERE correo = %(correo)s;"
        results = connectToMySQL(Usuario.db_name).query_db(query, user)
        if not EMAIL_REGEX.match(user['correo']):
            flash("Invalid Email!!!", "register")
            is_valid = False
        if len(user['contrasena']) < 4:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        return is_valid
