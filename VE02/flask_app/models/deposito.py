from flask_app.config.mysqlconnection import connectToMySQL



class Deposito:
    db_name = "boveda"

    def __init__(self, data):
        self.id_deposito = data['id_deposito']
        self.descripcion = data['descripcion']
        self.creado_en = data['creado_en']
        self.id_usuario = data['id_usuario']
        self.nombres = data['nombres']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO depositos (descripcion,creado_en,id_usuario) VALUES (%(descripcion)s,now(),%(id_usuario)s)"
        print(query)
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM depositos;"
        depositos_from_db = connectToMySQL(cls.db_name).query_db(query)
        depositos = []
        for d in depositos_from_db:
            depositos.append(cls(d))
        return depositos

    @classmethod
    def get_by_name(cls):
        query = "SELECT d.id_deposito, d.descripcion, d.creado_en, d.id_usuario, u.nombres as nombres FROM depositos d join usuario u ON u.id_usuario = d.id_usuario;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_depositos = []
        for row in results:
            all_depositos.append(cls(row))
            print(all_depositos)
        return all_depositos

    @classmethod
    def update(cls, data):
        query = "UPDATE depositos SET descripcion=%(descripcion)s WHERE id_deposito = %(id_deposito)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM depositos WHERE id_deposito = %(id_deposito)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
