from flask import request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash

from app import app
from auth import cargo_required
from models.conexao import Session
from models.administrador_model import Funcionarios

# Cargos aceitos no cadastro (devem bater com DASHBOARD_POR_CARGO do main.py)
CARGOS_VALIDOS = {"administrador", "recepcionista", "tecnico", "analista"}


def normalizar_cargo(cargo):
    return (cargo or "").strip().lower()


# ---------------------------------------------------------------
# FORMULÁRIO DE NOVO FUNCIONÁRIO
# ---------------------------------------------------------------
@app.route("/funcionario/novo")
@cargo_required("administrador")
def inserir_funcionario():
    return render_template("funcionarios.html")


# ---------------------------------------------------------------
# CRIAR
# ---------------------------------------------------------------
@app.route("/funcionario/create", methods=["POST"])
@cargo_required("administrador")
def criar_funcionario():
    cpf = request.form.get("cpf", "").strip()
    nome = request.form.get("nome", "").strip()
    data = request.form.get("data")
    sexo = request.form.get("sexo")
    telefone = request.form.get("telefone", "").strip()
    email = request.form.get("email", "").strip()
    senha = request.form.get("senha", "")
    endereco = request.form.get("endereco", "").strip()
    cidade = request.form.get("cidade", "").strip()
    cargo = normalizar_cargo(request.form.get("cargo"))

    if not email or not senha:
        flash("Email e senha são obrigatórios.")
        return redirect(url_for("listar_funcionarios"))

    if cargo not in CARGOS_VALIDOS:
        flash("Cargo inválido.")
        return redirect(url_for("listar_funcionarios"))

    with Session() as db:
        # Impede dois funcionários com o mesmo email
        if db.query(Funcionarios).filter(Funcionarios.email == email).first():
            flash("Já existe um funcionário com esse email.")
            return redirect(url_for("listar_funcionarios"))

        novo = Funcionarios(
            cpf=cpf,
            nome=nome,
            data=data,
            sexo=sexo,
            telefone=telefone,
            email=email,
            senha=generate_password_hash(senha),  # <- hash, nunca texto puro
            endereco=endereco,
            cidade=cidade,
            cargo=cargo,
        )
        db.add(novo)
        db.commit()

    return redirect(url_for("listar_funcionarios"))


# ---------------------------------------------------------------
# LISTAR
# ---------------------------------------------------------------
@app.route("/funcionario/lista")
@cargo_required("administrador")
def listar_funcionarios():
    with Session() as db:
        funcionarios = db.query(Funcionarios).all()
        return render_template("funcionarios.html", funcionarios=funcionarios)


# ---------------------------------------------------------------
# DELETAR
# ---------------------------------------------------------------
@app.route("/funcionario/deletar/<int:item_id>")
@cargo_required("administrador")
def deletar_funcionario(item_id):
    # Impede o administrador de apagar a própria conta
    if item_id == session.get("user_id"):
        flash("Você não pode excluir o seu próprio usuário.")
        return redirect(url_for("listar_funcionarios"))

    with Session() as db:
        item = db.get(Funcionarios, item_id)
        if item:
            db.delete(item)
            db.commit()

    return redirect(url_for("listar_funcionarios"))


# ---------------------------------------------------------------
# EDITAR (formulário)
# ---------------------------------------------------------------
@app.route("/funcionario/editar/<int:id>")
@cargo_required("administrador")
def editar_funcionario(id):
    with Session() as db:
        funcionario = db.get(Funcionarios, id)
        if not funcionario:
            flash("Funcionário não encontrado.")
            return redirect(url_for("listar_funcionarios"))
        return render_template("funcionario/atualizar.html", funcionario=funcionario)


# ---------------------------------------------------------------
# EDITAR (salvar)
# ---------------------------------------------------------------
@app.route("/funcionario/editar", methods=["POST"])
@cargo_required("administrador")
def editar_funcionario_salvar():
    id = request.form.get("id", type=int)
    email = request.form.get("email", "").strip()
    cargo = normalizar_cargo(request.form.get("cargo"))
    nova_senha = request.form.get("senha", "")

    if cargo not in CARGOS_VALIDOS:
        flash("Cargo inválido.")
        return redirect(url_for("listar_funcionarios"))

    with Session() as db:
        funcionario = db.get(Funcionarios, id)
        if not funcionario:
            flash("Funcionário não encontrado.")
            return redirect(url_for("listar_funcionarios"))

        # Email já usado por OUTRO funcionário?
        duplicado = (
            db.query(Funcionarios)
            .filter(Funcionarios.email == email, Funcionarios.id != id)
            .first()
        )
        if duplicado:
            flash("Esse email já pertence a outro funcionário.")
            return redirect(url_for("listar_funcionarios"))

        funcionario.cpf = request.form.get("cpf", "").strip()
        funcionario.nome = request.form.get("nome", "").strip()
        funcionario.data = request.form.get("data")
        funcionario.sexo = request.form.get("sexo")
        funcionario.telefone = request.form.get("telefone", "").strip()
        funcionario.email = email
        funcionario.endereco = request.form.get("endereco", "").strip()
        funcionario.cidade = request.form.get("cidade", "").strip()
        funcionario.cargo = cargo

        # Só troca a senha se o campo foi preenchido
        if nova_senha:
            funcionario.senha = generate_password_hash(nova_senha)

        db.commit()

        # Mantém o nome/cargo da sessão atualizados se editou a si mesmo
        if funcionario.id == session.get("user_id"):
            session["user_name"] = funcionario.nome
            session["cargo"] = cargo

    return redirect(url_for("listar_funcionarios"))