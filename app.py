import os

from flask import Flask, request
from flaskext.mysql import MySQL
from flask import jsonify

app = Flask(__name__)
app.run(port=os.environ['PORT'])

mysql = MySQL()
mysql.init_app(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'tareas_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# traer tareas

@app.route("/", methods=['GET'])
def get_all():
    with mysql.connect() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM tarea")
            data = cursor.fetchall()

            return jsonify(data)

# traer un taras
@app.route("/<int:id>")
def get_one(id):
    with mysql.connect() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM tarea WHERE id = %s", (id,))
            data = cursor.fetchone()

            return jsonify(data)

# guardar un tareas
@app.route("/nuevo", methods=['GET','POST'])
def save():
    if request.method == 'POST':
        with mysql.connect() as conexion:
            with conexion.cursor() as cursor:
                data = request.get_json()
                tarea = data['tarea']
                cursor.execute("INSERT INTO tarea(tarea) VALUES (%s)", (tarea,))
                conexion.commit()

                return jsonify(tarea)

# editar un tareas
@app.route("/editar/<int:id>", methods=['PUT'])
def editar(id):
    if request.method == 'PUT':
        with mysql.connect() as conexion:
            with conexion.cursor() as cursor:
                data = request.get_json()
                tarea = data['tarea']
                cursor.execute("UPDATE tarea SET tarea = %s WHERE id = %s", (tarea, id))
                conexion.commit()

                return jsonify(tarea)

# eliminar tareas
@app.route("/eliminar/<int:id>",methods=['DELETE'])
def eliminar(id):
    if request.method == 'DELETE':
        with mysql.connect() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM tarea WHERE id = %s", (id,))
                conexion.commit()

                return jsonify({'msg': 'Registro eliminado'})