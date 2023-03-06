from flask_app.config.mysqlconnection import connectToMySQL


class Entrada:
    db_name = "boveda"

    def __init__(self, data):
        self.id_entrada = data['id_entrada']
        self.referencia = data['referencia']
        self.fecha = data['fecha']
        self.caratula = data['caratula']
        self.instrumento = data['instrumento']
        self.tipo = data['tipo']
        self.estado = data['estado']
        self.observacion = data['observacion']
        self.nro_oficio = data['nro_oficio']
        self.id_usuario = data['id_usuario']
        self.id_ubicacion = data['id_ubicacion']
        self.nombres = data['nombres']
        self.descripcion = data['descripcion']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO entradas (referencia,fecha,caratula,instrumento,tipo,estado,observacion,nro_oficio," \
                "id_usuario,id_ubicacion) VALUES (%(referencia)s,now(),%(caratula)s,%(instrumento)s,%(tipo)s,%(estado)s," \
                "%(observacion)s,%(nro_oficio)s,%(id_usuario)s,%(id_ubicacion)s)"
        print(query)
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM entradas;"
        entradas_from_db = connectToMySQL(cls.db_name).query_db(query)
        entradas = []
        for e in entradas_from_db:
            entradas.append(cls(e))
        return entradas

    @classmethod
    def get_by_name(cls):
        query = "SELECT e.*, u.nombres as nombres, ub.descripcion as descripcion FROM entradas e " \
                "join usuario u join ubicaciones ub ON e.id_usuario = u.id_usuario and" \
                " e.id_ubicacion = ub.id_ubicacion WHERE e.estado LIKE 'activo';"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_entradas = []
        for row in results:
            all_entradas.append(cls(row))
        return all_entradas

    @classmethod
    def update(cls, data):
        query = "UPDATE entradas SET referencia=%(referencia)s, caratula=%(caratula)s, instrumento=%(instrumento)s, " \
                "tipo=%(tipo)s, observacion=%(observacion)s, nro_oficio=%(nro_oficio)s," \
                " id_ubicacion=%(id_ubicacion)s WHERE id_entrada = %(id_entrada)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def desactivate(cls, data):
        query = "UPDATE entradas SET estado= 'inactivo' WHERE id_entrada = %(id_entrada)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
