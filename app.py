import time

import psycopg2
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

cache = psycopg2.connect(
    database="proyectoSO",
    user="root",
    password="mysecretpassword",
    host="postgresqldb"

)

def get_hit_count():
    retries = 5
    while True:
        try:
            with cache:
                with cache.cursor() as curs:
                    curs.execute('''UPDATE "contar" set contador = contador + 1''')
                    curs.execute('''SELECT * FROM "contar"''')
                    return curs.fetchall()[0][0]
        except psycopg2.OperationalError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/', methods=['GET'])
def hello():
    count = get_hit_count()
    return 'Hello World from docker! I have been seen {} times.\n'.format(count)

@app.route('/reset', methods=['DELETE'])
def resetcount():
    with cache:
                with cache.cursor() as curs:
                    curs.execute('''DELETE FROM "contar"''')
                    curs.execute('''INSERT INTO "contar" VALUES (0)''')
                    return jsonify({'Message':'El contador fue reiniciado.'})

@app.route('/asignar/<id>', methods=['POST'])
def postcount(id):
    with cache:
                with cache.cursor() as curs:
                    curs.execute('''UPDATE "contar" set contador = {}'''.format(id))
                    return jsonify({'Message':'El nuevo valor fue asignado.'})

@app.route('/actualizar/<id>', methods=['PUT'])
def putcount(id):
    with cache:
                with cache.cursor() as curs:
                    curs.execute('''UPDATE "contar" set contador = {}'''.format(id))
                    return jsonify({'Message':'El contador fue actualizado'})

@app.route('/obtener', methods=['GET'])
def getcount():
    with cache:
                with cache.cursor() as curs:
                    curs.execute('''SELECT * FROM "contar"''')
                    return jsonify({'Message': 'El valor actual del contador es {}'.format(curs.fetchall()[0][0])})

