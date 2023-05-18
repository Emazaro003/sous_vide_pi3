# , jsonify, request
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/ligar", methods=["POST", "GET"])
def ligar():
    return home()


app.run()
