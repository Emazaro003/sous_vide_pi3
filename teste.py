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
        host="db4free.net",
        user="grupo4",
        passwd="admin123",
        database="pi3_sous_vide_g4",
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
        nomeReceita = request.form["string"]
        receita = pegaReceita(nomeReceita)
        # Faça algo com a string recebida, por exemplo, retornar ela como uma resposta
        return render_template("receitas.html", receita=receita, aquecida=aquecida)
    if cnx == "":
        conecta_BD()
    receita = receitas()
    return render_template("index.html", receitas=receita)


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


@app.route("/salva-temperatura", methods=["GET"])
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


@app.route("/desligar", methods=["GET"])
def desligar():
    # GPIO.setup(porta_rele, GPIO.IN)
    return jsonify({"response": "execuado"})


@app.route("/ligar", methods=["GET"])
def ligar():
    # GPIO.setup(porta_rele, GPIO.OUT)
    # GPIO.output(porta_rele, 1)
    return jsonify({"response": "execuado"})


@app.route("/temperatura", methods=["GET"])
def getTemp():
    return jsonify(
        {
            "temperatura_sensor_1": temp.read_temp_sens1(),
            "temperatura_sensor_2": temp.read_temp_sens2(),
        }
    )


app.run(host="192.168.18.144")  # host="192.168.146.57", port="8080"
