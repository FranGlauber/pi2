from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

# Segurança e autenticação
from app import *
from auth import login_required, cargo_required

# MODELS
from models.conexao import Base, Session, engine
from models.administrador_model import *
from models.paciente_model import *

# CONTROLLERS
from controllers.administrador_controller import *
from controllers.paciente_controller import *


# Mapeia cada cargo para a rota do seu dashboard.
# Ajuste as chaves para ficarem IGUAIS ao que está salvo na coluna cargo.
DASHBOARD_POR_CARGO = {
    "administrador": "administracao",
    "recepcionista": "recepcao",
    "tecnico": "tecnico",
    "analista": "analista",
}


def normalizar_cargo(cargo):
    """Evita erro por maiúscula/minúscula ou espaço sobrando no banco."""
    return (cargo or "").strip().lower()


# ---------------------------------------------------------------
# LOGIN / LOGOUT
# ---------------------------------------------------------------
@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    # Quem já está logado vai direto para o seu painel
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    senha = request.form.get("senha", "")

    if not email or not senha:
        return render_template("login.html", error="Preencha email e senha.")

    with Session() as db:
        user = db.query(Funcionarios).filter(Funcionarios.email == email).first()

        # 1) usuário existe  2) senha confere com o hash
        if not user or not check_password_hash(user.senha, senha):
            return render_template("login.html", error="Email ou senha incorretos.")

        # 3) cargo precisa ser um dos cargos conhecidos
        cargo = normalizar_cargo(user.cargo)
        if cargo not in DASHBOARD_POR_CARGO:
            return render_template(
                "login.html",
                error="Seu cargo não tem acesso ao sistema. Fale com o administrador."
            )

        session.clear()
        session["user_id"] = user.id
        session["user_name"] = user.nome
        session["cargo"] = cargo

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@login_required
def dashboard():
    """Redireciona cada usuário para o painel do seu cargo."""
    destino = DASHBOARD_POR_CARGO.get(session.get("cargo"))
    if not destino:
        session.clear()
        return redirect(url_for("login"))
    return redirect(url_for(destino))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------
# ADMINISTRADOR
# ---------------------------------------------------------------
@app.route("/administracao")
@cargo_required("administrador")
def administracao():
    return render_template("dashboard_admin.html")


# ---------------------------------------------------------------
# RECEPÇÃO
# ---------------------------------------------------------------
@app.route("/recepcao")
@cargo_required("recepcionista", "administrador")
def recepcao():
    with Session() as db:
        pacientes = db.query(Paciente).order_by(Paciente.nome).all()
        return render_template("dashboard_recepcao.html", pacientes=pacientes)


@app.route("/pacientes")
@cargo_required("recepcionista", "administrador")
def pacientes():
    return render_template("pacientes.html")


@app.route("/solicitar_exames")
@cargo_required("recepcionista", "administrador")
def solicitar_exames():
    return render_template("solicitar_exames.html")


@app.route("/situacao_exames")
@cargo_required("recepcionista", "administrador")
def situacao_exames():
    return render_template("situacao_exames.html")


# ---------------------------------------------------------------
# TÉCNICO
# ---------------------------------------------------------------
@app.route("/tecnico")
@cargo_required("tecnico", "administrador")
def tecnico():
    return render_template("dashboard_tecnico.html")


@app.route("/registrar_coletas")
@cargo_required("tecnico", "administrador")
def registrar_coletas():
    return render_template("registrar_coletas.html")


@app.route("/coletas_realizadas")
@cargo_required("tecnico", "administrador")
def coletas_realizadas():
    return render_template("coletas_realizadas.html")


@app.route("/perfil_tecnico")
@cargo_required("tecnico", "administrador")
def perfil_tecnico():
    return render_template("perfil_tecnico.html")


# ---------------------------------------------------------------
# ANALISTA
# ---------------------------------------------------------------
@app.route("/analista")
@cargo_required("analista", "administrador")
def analista():
    return render_template("dashboard_analista.html")


@app.route("/coletas_recebidas")
@cargo_required("analista", "administrador")
def coletas_recebidas():
    return render_template("coletas_recebidas.html")


@app.route("/registro_resultados")
@cargo_required("analista", "administrador")
def registro_resultados():
    return render_template("registro_resultados.html")


@app.route("/registrar_exames")
@cargo_required("analista", "administrador")
def registrar_exames():
    return render_template("registrar_exames.html")


@app.route("/emissao_laudos")
@cargo_required("analista", "administrador")
def emissao_laudos():
    return render_template("emissao_laudos.html")


@app.route("/historico_exames")
@cargo_required("analista", "administrador")
def historico_exames():
    return render_template("historico_exames.html")


@app.route("/perfil_analista")
@cargo_required("analista", "administrador")
def perfil_analista():
    return render_template("perfil_analista.html")


# ---------------------------------------------------------------
# COMUM A TODOS OS LOGADOS
# ---------------------------------------------------------------
@app.route("/perfil")
@login_required
def perfil():
    return render_template("perfil.html")


if __name__ == "__main__":
    app.run(debug=True)