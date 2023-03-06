from flask_app.config.mysqlconnection import connectToMySQL


class Ubicacion:
    db_name = "boveda"

    def __init__(self, data):
        self.id_ubicacion = data['id_ubicacion']
        self.descripcion = data['descripcion']
        self.estado = data['estado']
        self.creado_en = data['creado_en']
        self.id_usuario = data['id_usuario']
        self.id_deposito = data['id_deposito']
        self.nombres = data['nombres']
        self.descri = data['descri']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO ubicaciones (descripcion,estado,creado_en,id_usuario,id_deposito) VALUES " \
                "(%(descripcion)s,%(estado)s,now(),%(id_usuario)s,%(id_deposito)s)"
        print(query)
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ubicaciones;"
        ubicaciones_from_db = connectToMySQL(cls.db_name).query_db(query)
        ubicaciones = []
        for u in ubicaciones_from_db:
            ubicaciones.append(cls(u))
        return ubicaciones

    @classmethod
    def get_by_name(cls):
        query = "SELECT u.id_ubicacion, u.descripcion, u.estado, u.creado_en, u.id_usuario, u.id_deposito, " \
                "us.nombres as nombres, d.descripcion as descri FROM ubicaciones u join usuario us" \
                " join depositos d ON u.id_usuario = us.id_usuario and u.id_deposito = d.id_deposito;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_ubicaciones = []
        for row in results:
            all_ubicaciones.append(cls(row))
        return all_ubicaciones

    @classmethod
    def update(cls, data):
        query = "UPDATE ubicaciones SET descripcion=%(descripcion)s,estado=%(estado)s,id_deposito=%(id_deposito)s " \
                "WHERE id_ubicacion = %(id_ubicacion)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM ubicaciones WHERE id_ubicacion = %(id_ubicacion)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
