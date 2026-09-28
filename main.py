from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from datetime import datetime

from controllers.paciente_controller import *

app = Flask(__name__)
app.secret_key = "laboratorio-chave-secreta"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/dashboard_tecnico")
def dashboard_tecnico():
    return render_template("dashboard_tecnico.html")


@app.route("/registrar_coletas")
def registrar_coletas():
    return render_template("registrar_coletas.html")


@app.route("/coletas_realizadas")
def coletas_realizadas():
    return render_template("coletas_realizadas.html")


@app.route("/perfil_tecnico")
def perfil_tecnico():
    return render_template("perfil_tecnico.html")


@app.route("/administracao")
def administracao():
    return render_template("dashboard_admin.html")


if __name__ == "__main__":
    app.run(debug=True)