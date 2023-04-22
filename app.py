import time

import mysql.connector
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request

import temp

cnx = ''
cursor = ''
GPIO.setmode(GPIO.BOARD)
app = Flask(__name__)
porta_rele = 12


def conecta_BD():
    global cnx
    global cursor
    cnx = mysql.connector.connect(host="db4free.net",
                                  user="grupo4",
                                  passwd="admin123",
                                  database="pi3_sous_vide_g4")
    cursor = cnx.cursor()
    return cursor


def desconecta_BD():
    global cnx
    global cursor
    if cnx != '':
        print("ta saindo")
        cursor.close()
        cnx.commit()
        cnx.close()


def tempo_receita(receita):
    global cnx
    global cursor
    if cnx.is_connected():
        cursor.execute('SELECT * FROM Teste')
        tempo_receita = cursor.fetchone()[0]
    return tempo_receita


def desligar():
    GPIO.output(porta_rele, 0)


@app.route("/ligar", methods=['POST'])
def ligar():
    receita = request.json[1]
    tempo = tempo_receita(receita)
    GPIO.setup(porta_rele, GPIO.OUT)
    GPIO.output(porta_rele, 1)
    time.sleep(tempo)
    desligar()
    return True


@app.route("/temperatura", methods=['GET'])
def getTemp():
    return jsonify({
        'temperatura_sensor_1': temp.read_temp_sens1,
        'temperatura_sensor_2': temp.read_temp_sens2,
    })


app.run()
