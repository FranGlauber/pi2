from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/recepcao")
def recepcao():
    return render_template("recepcao.html")


@app.route("/pacientes")
def pacientes():
    return render_template("pacientes.html")


@app.route("/solicitar_exames")
def solicitar_exames():
    return render_template("solicitar_exames.html")

@app.route("/situacao_exames")
def situacao_exames():
    return render_template("situacao_exames.html")

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")


@app.route("/administracao")
def administracao():
    return render_template("dashboard_admin.html")


if __name__ == "__main__":
    app.run(debug=True)