import mysql.connector

# import RPi.GPIO as GPIO
from flask import Flask, jsonify, render_template, request

# import temp

cnx = ""
cursor = ""
# GPIO.setmode(GPIO.BOARD)
app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
porta_rele = 29
id_sensor1 = 1
id_sensor2 = 2


def conecta_BD():
    global cnx
    global cursor
    cnx = mysql.connector.connect(
        host="***",
        user="***",
        passwd="***",
        database="***",
    )
    cursor = cnx.cursor()


@app.route("/desconectar-banco", methods=["PSOT", "GET"])
def desconecta_BD():
    global cnx
    global cursor
    if cnx != "":
        print("ta saindo")
        cursor.close()
        cnx.commit()
        cnx.close()
    return jsonify({"response": "execuado"})


# ---------------MAIN---------------------------
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        aquecida = False  # panelaAqueceu()
        if request.form["aquecida"] != "":
            aquecida = True
            temperaturaReceita = request.form["temperatura"]
            tempoReceita = request.form["tempo"]
            tipoTempoReceita = request.form["tempo_tipo"]
            print(
                f"{temperaturaReceita} {tempoReceita} {type(tempoReceita)} {tipoTempoReceita}"
            )
            ligar(temperaturaReceita, tempoReceita, tipoTempoReceita)
        nomeReceita = request.form["string"]
        receita = pegaReceita(nomeReceita)
        # Faça algo com a string recebida, por exemplo, retornar ela como uma resposta
        return render_template("receitas.html", receita=receita, aquecida=aquecida)
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


def desligar():
    # GPIO.setup(porta_rele, GPIO.IN)
    return jsonify({"response": "execuado"})


def getTemp():
    temperaturas = {
        "temperatura_sensor_1": temp.read_temp_sens1(),
        "temperatura_sensor_2": temp.read_temp_sens2(),
    }
    return temperaturas


def ligar(temperatura, tempo, tipoTempo):
    temperaturas = getTemp()

    if temperaturas["temperatura_sensor_1"] < temperatura:
        GPIO.setup(porta_rele, GPIO.OUT)
        while temperaturas["temperatura_sensor_1"] < temperatura:
            time.sleep(10)
            temperaturas = getTemp()


app.run(host="127.0.0.1")  # host="192.168.146.57", port="8080"
