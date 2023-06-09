import time

import mysql.connector
import RPi.GPIO as GPIO
from flask import Flask, jsonify, render_template, request

import temp

cnx = ""
cursor = ""
cancela = False
resistenciaTaLigada = True
podeInserir = False
GPIO.setmode(GPIO.BOARD)
app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
porta_rele = 29
id_sensor1 = 1
id_sensor2 = 2


def conecta_BD():
    global cnx
    global cursor
    cnx = mysql.connector.connect(
        host="*",
        user="*",
        passwd="*",
        database="*",
    )
    cursor = cnx.cursor()
    print("Conectou-se ao banco")


@app.route("/desconectar-banco", methods=["PSOT", "GET"])
def desconecta_BD():
    global cnx
    global cursor
    if cnx != "":
        print("Desconectou-se do banco")
        cursor.close()
        cnx.commit()
        cnx.close()
    return jsonify({"response": "execuado"})


# ---------------MAIN---------------------------
@app.route("/", methods=["POST", "GET"])
def index():
    global cancela
    global podeInserir
    cancela = False

    desligar()
    if request.method == "POST":
        podeInserir = False
        aquecida = False
        if request.form["aquecida"] == "aquecida":
            aquecida = True
            temperaturaReceita = float(request.form["temperatura"])
            tempoReceita = float(request.form["tempo"])
            tipoTempoReceita = request.form["tempo_tipo"]
            aquecer(temperaturaReceita, tempoReceita, tipoTempoReceita)
        if request.form["cancela"] == "cancela":
            cancela = True
            aquecida = False
        nomeReceita = request.form["string"]
        receita = pegaReceita(nomeReceita)
        return render_template(
            "receitas.html",
            receita=receita,
            aquecida=aquecida,
            cancela=cancela,
            inserir=podeInserir,
        )

    if cnx == "":
        conecta_BD()
    receita = receitas()
    return render_template("index.html", receitas=receita)


# -----------------------------------------------


@app.route("/receitas", methods=["PSOT", "GET"])
def receitas():
    if cnx == "":
        conecta_BD()
    cursor.execute("SELECT * FROM Tabela_coccção")
    receitas = cursor.fetchall()
    return receitas  # jsonify({"receitas": receitas})


def pegaReceita(rec):
    if cnx == "":
        conecta_BD()
    cursor.execute(f"SELECT * FROM Tabela_coccção where Nome = '{rec}';")
    receita = cursor.fetchone()
    return receita  # jsonify({"receitas": receitas})


def salva_temperatura():
    global cnx
    global cursor
    if cnx == "":
        conecta_BD()
    cursor.execute(
        f"insert into Teste (id, temocelcius) values ({id_sensor1}, {temp.read_temp_sens1()});"
    )
    cursor.execute(
        f"insert into Teste (id, temocelcius) values ({id_sensor2}, {temp.read_temp_sens2()});"
    )
    cnx.commit()
    return jsonify({"response": "execuado"})


@app.route("/desligar", methods=["PSOT", "GET"])
def desligar():
    global porta_rele
    global resistenciaTaLigada

    if resistenciaTaLigada:
        GPIO.setup(porta_rele, GPIO.IN)
        resistenciaTaLigada = False
    return jsonify({"response": "execuado"})


def ligar():
    global porta_rele
    global resistenciaTaLigada

    if not resistenciaTaLigada:
        GPIO.setup(porta_rele, GPIO.OUT)
        resistenciaTaLigada = True


@app.route("/temp", methods=["PSOT", "GET"])
def getTemp():
    temperaturas = {
        "temperatura_sensor_1": temp.read_temp_sens1(),
        "temperatura_sensor_2": temp.read_temp_sens2(),
    }
    return temperaturas


def tempEMenor(tempReceita):
    temperaturas = getTemp()
    if temperaturas["temperatura_sensor_1"] < tempReceita:
        return True
    else:
        return False


def tempoControle(tempo, tipoTempo, tempReceita):
    global cancela
    tempReceita = tempReceita * 0.9  # Olhar sempre para 90% da temperatura
    # if tipoTempo == "min":
    cont = 0
    while cont < ((tempo * 60) / 3):
        temperaturaEMenor = tempEMenor(tempReceita)
        if cancela:
            desligar()
            return
        if temperaturaEMenor:
            ligar()
        if not temperaturaEMenor:
            desligar()
        cont = cont + 1


def aquecer(tempReceita, tempo, tipoTempo):
    global cancela
    global podeInserir

    tempSensores = getTemp()
    if tempSensores["temperatura_sensor_1"] < tempReceita:
        if cancela:
            desligar()
            return
        ligar()
        while tempEMenor(tempReceita):
            time.sleep(10)
        desligar()
    podeInserir = True
    tempoControle(tempo, tipoTempo, tempReceita)


app.run(host="127.0.0.1")  # host="192.168.57.57", port="8080"
