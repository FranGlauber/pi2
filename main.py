from flask import Flask, render_template, request, redirect, url_for, session, flash
#from datetime import datetime

from controllers.paciente_controller import *

app = Flask(__name__)
app.secret_key = "laboratorio-chave-secreta"

@app.route("/coletas_realizadas")
def coletas_realizadas():
    return render_template("coletas_realizadas.html")

@app.route("/administracao")
def administracao():
    return render_template("dashboard_admin.html")

@app.route("/recepcao")
def recepcao():
    return render_template("dashboard_recepcao.html")

@app.route("/tecnico")
def tecnico():
    return render_template("dashboard_tecnico.html")

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/pacientes")
def pacientes():
    return render_template("pacientes.html")

@app.route("/perfil_tecnico")
def perfil_tecnico():
    return render_template("perfil_tecnico.html")

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")

@app.route("/registrar_coletas")
def registrar_coletas():
    return render_template("registrar_coletas.html")

@app.route("/registrar_exames")
def registrar_exames():
    return render_template("registrar_exames.html")

@app.route("/situacao_exames")
def situacao_exames():
    return render_template("situacao_exames.html")

@app.route("/solicitar_exames")
def solicitar_exames():
    return render_template("solicitar_exames.html")

@app.route("/logout")
def logout():
    #session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
