from flask import Flask, render_template, request, redirect, url_for, session, flash

# Segurança e autenticação
from app import *
from auth import login_required

# MODELS(Modelos das tabelas do banco de dados)
from models.conexao import Base, Session, engine
from models.administrador_model import *
from models.analista_model import *
from models.paciente_model import *
from models.recepcao_model import *
from models.tecnico_model import *

# CONTROLLERS (Funções do CRUD)
from controllers.administrador_controller import *
from controllers.analista_controller import *
from controllers.paciente_controller import *
from controllers.recepcao_controller import *
from controllers.tecnico_controller import *

# ROTAS (URLs do sistema)

@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get("email")
    senha = request.form.get("senha")


    db = Session()
    adm = db.query(Funcionarios).filter(Funcionarios.email==email, Funcionarios.senha==senha, Funcionarios.cargo=="administrador").first()
    rec = db.query(Funcionarios).filter(Funcionarios.email==email, Funcionarios.senha==senha, Funcionarios.cargo=="recepcionista").first()
    ana = db.query(Funcionarios).filter(Funcionarios.email==email, Funcionarios.senha==senha, Funcionarios.cargo=="analista").first()
    tec = db.query(Funcionarios).filter(Funcionarios.email==email, Funcionarios.senha==senha, Funcionarios.cargo=="tecnico").first()
    #pac = db.query(Paciente).filter(Paciente.email==email, Paciente.senha==senha).first()


    if adm:
        session['user_id'] = adm.id
        session['user_name'] = adm.nome
        return render_template('dashboard_admin.html')
    elif rec:
        session['user_id'] = rec.id
        session['user_name'] = rec.nome
        return render_template('dashboard_recepcao.html')
    elif ana:
        session['user_id'] = ana.id
        session['user_name'] = ana.nome
        return render_template('dashboard_analista.html')
    elif tec:
        session['user_id'] = tec.id
        session['user_name'] = tec.nome
        return render_template('dashboard_tecnico.html')
    else:
        return render_template('index.html', error="Email ou senha incorretos.")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

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


@app.route("/analista")
def analista():
    return render_template("dashboard_analista.html")

@app.route("/coletas_recebidas")
def coletas_recebidas():
    return render_template("coletas_recebidas.html")

@app.route("/registro_resultados")
def registro_resultados():
    return render_template("registro_resultados.html")

@app.route("/emissao_laudos")
def emissao_laudos():
    return render_template("emissao_laudos.html")

@app.route("/historico_exames")
def historico_exames():
    return render_template("historico_exames.html")

@app.route("/perfil_analista")
def perfil_analista():
    return render_template("perfil_analista.html")


if __name__ == "__main__":
    app.run(debug=True)
