from flask import Flask, render_template, request, redirect, url_for, session, flash
from database.database import conectar, criar_banco
from controllers.paciente_controller import *
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = "laboratorio-chave-secreta"

criar_banco()


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


def recepcionista_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))

        if session.get("perfil") != "recepcionista":
            return "Acesso não autorizado", 403

        return func(*args, **kwargs)
    return wrapper


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        conexao = conectar()

        usuario = conexao.execute(
            """
            SELECT id, nome, email, senha, perfil
            FROM usuarios
            WHERE email = ? AND senha = ?
            """,
            (email, senha)
        ).fetchone()

        conexao.close()

        if usuario:
            session["usuario_id"] = usuario["id"]
            session["nome"] = usuario["nome"]
            session["email"] = usuario["email"]
            session["perfil"] = usuario["perfil"]

            if usuario["perfil"] == "recepcionista":
                return redirect(url_for("recepcao"))

            return redirect(url_for("login"))

        flash("E-mail ou senha inválidos.", "erro")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/recepcao")
@recepcionista_required
def recepcao():
    conexao = conectar()

    total_pacientes = conexao.execute(
        "SELECT COUNT(*) AS total FROM pacientes"
    ).fetchone()["total"]

    solicitacoes_hoje = conexao.execute(
        """
        SELECT COUNT(*) AS total
        FROM solicitacoes
        WHERE date(data_solicitacao) = date('now', 'localtime')
        """
    ).fetchone()["total"]

    aguardando_coleta = conexao.execute(
        """
        SELECT COUNT(*) AS total
        FROM solicitacoes
        WHERE status = 'Aguardando coleta'
        """
    ).fetchone()["total"]

    em_andamento = conexao.execute(
        """
        SELECT COUNT(*) AS total
        FROM solicitacoes
        WHERE status = 'Em andamento'
        """
    ).fetchone()["total"]

    concluidos = conexao.execute(
        """
        SELECT COUNT(*) AS total
        FROM solicitacoes
        WHERE status = 'Concluído'
        """
    ).fetchone()["total"]

    pacientes_recentes = conexao.execute(
        """
        SELECT
            p.id,
            p.nome,
            p.cpf,
            p.telefone,
            (
                SELECT s.data_solicitacao
                FROM solicitacoes s
                WHERE s.paciente_id = p.id
                ORDER BY s.id DESC
                LIMIT 1
            ) AS ultima_solicitacao,
            COALESCE(
                (
                    SELECT s.status
                    FROM solicitacoes s
                    WHERE s.paciente_id = p.id
                    ORDER BY s.id DESC
                    LIMIT 1
                ),
                'Sem solicitação'
            ) AS status
        FROM pacientes p
        ORDER BY p.id DESC
        LIMIT 5
        """
    ).fetchall()

    conexao.close()

    return render_template(
        "recepcao.html",
        total_pacientes=total_pacientes,
        solicitacoes_hoje=solicitacoes_hoje,
        aguardando_coleta=aguardando_coleta,
        em_andamento=em_andamento,
        concluidos=concluidos,
        pacientes_recentes=pacientes_recentes
    )


@app.route("/pacientes", methods=["GET", "POST"])
@recepcionista_required
def pacientes():
    conexao = conectar()

    if request.method == "POST":
        dados = (
            request.form.get("nome", "").strip(),
            request.form.get("cpf", "").strip(),
            request.form.get("nascimento", "").strip(),
            request.form.get("sexo", "").strip(),
            request.form.get("telefone", "").strip(),
            request.form.get("email", "").strip(),
            request.form.get("cep", "").strip(),
            request.form.get("endereco", "").strip(),
            request.form.get("numero", "").strip(),
            request.form.get("complemento", "").strip(),
            request.form.get("bairro", "").strip(),
            request.form.get("cidade", "").strip(),
            request.form.get("estado", "").strip()
        )

        if not dados[0] or not dados[1] or not dados[2] or not dados[3]:
            flash("Preencha os campos obrigatórios.", "erro")
        else:
            try:
                conexao.execute(
                    """
                    INSERT INTO pacientes (
                        nome, cpf, data_nascimento, sexo, telefone,
                        email, cep, endereco, numero, complemento,
                        bairro, cidade, estado
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    dados
                )
                conexao.commit()
                flash("Paciente cadastrado com sucesso.", "sucesso")
            except Exception as erro:
                flash("CPF já cadastrado ou dados inválidos.", "erro")

    busca = request.args.get("busca", "").strip()

    if busca:
        pacientes_lista = conexao.execute(
            """
            SELECT *
            FROM pacientes
            WHERE nome LIKE ?
               OR cpf LIKE ?
            ORDER BY nome
            """,
            (f"%{busca}%", f"%{busca}%")
        ).fetchall()
    else:
        pacientes_lista = conexao.execute(
            """
            SELECT *
            FROM pacientes
            ORDER BY nome
            """
        ).fetchall()

    conexao.close()

    return render_template(
        "pacientes.html",
        pacientes=pacientes_lista
    )


@app.route("/solicitar_exames", methods=["GET", "POST"])
@recepcionista_required
def solicitar_exames():
    conexao = conectar()

    if request.method == "POST":
        paciente_id = request.form.get("paciente_id", "").strip()
        data_solicitacao = request.form.get("data_solicitacao", "").strip()
        observacoes = request.form.get("observacoes", "").strip()
        exame_ids = request.form.getlist("exame_ids")

        print("DEBUG SOLICITAÇÃO:", dict(request.form))
        print("PACIENTE:", paciente_id)
        print("DATA:", data_solicitacao)
        print("EXAMES:", exame_ids)

        if not paciente_id or not data_solicitacao:
            flash("Selecione o paciente e informe a data da solicitação.", "erro")

        elif not exame_ids:
            flash("Selecione pelo menos um exame.", "erro")

        else:
            paciente = conexao.execute(
                "SELECT id FROM pacientes WHERE id = ?",
                (paciente_id,)
            ).fetchone()

            if paciente is None:
                flash("Paciente não encontrado.", "erro")

            else:
                try:
                    cursor = conexao.execute(
                        """
                        INSERT INTO solicitacoes (
                            paciente_id,
                            usuario_id,
                            data_solicitacao,
                            status,
                            observacoes
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            paciente_id,
                            session["usuario_id"],
                            data_solicitacao,
                            "Aguardando coleta",
                            observacoes
                        )
                    )

                    solicitacao_id = cursor.lastrowid

                    for exame_id in exame_ids:
                        exame = conexao.execute(
                            "SELECT id FROM tipos_exames WHERE id = ?",
                            (exame_id,)
                        ).fetchone()

                        if exame:
                            conexao.execute(
                                """
                                INSERT INTO solicitacao_exames (
                                    solicitacao_id,
                                    exame_id
                                )
                                VALUES (?, ?)
                                """,
                                (solicitacao_id, exame["id"])
                            )

                    conexao.commit()

                    print("SOLICITAÇÃO SALVA:", solicitacao_id)

                    flash(
                        "Solicitação de exames salva com sucesso.",
                        "sucesso"
                    )

                    return redirect(url_for("situacao_exames"))

                except Exception as erro:
                    conexao.rollback()
                    print("ERRO AO SALVAR SOLICITAÇÃO:", repr(erro))

                    flash(
                        f"Erro ao salvar solicitação: {erro}",
                        "erro"
                    )

    pacientes_lista = conexao.execute(
        """
        SELECT id, nome, cpf, data_nascimento, telefone
        FROM pacientes
        ORDER BY nome
        """
    ).fetchall()

    exames_lista = conexao.execute(
        """
        SELECT id, nome, descricao
        FROM tipos_exames
        ORDER BY nome
        """
    ).fetchall()

    conexao.close()

    return render_template(
        "solicitar_exames.html",
        pacientes=pacientes_lista,
        exames=exames_lista
    )


@app.route("/situacao_exames")
@recepcionista_required
def situacao_exames():
    conexao = conectar()

    busca = request.args.get("busca", "").strip()
    status = request.args.get("status", "").strip()

    query = """
        SELECT
            s.id,
            s.data_solicitacao,
            s.status,
            s.observacoes,
            p.nome AS paciente,
            p.cpf,
            GROUP_CONCAT(e.nome, ', ') AS exames
        FROM solicitacoes s
        INNER JOIN pacientes p
            ON p.id = s.paciente_id
        INNER JOIN solicitacao_exames se
            ON se.solicitacao_id = s.id
        INNER JOIN tipos_exames e
            ON e.id = se.exame_id
        WHERE 1 = 1
    """

    parametros = []

    if busca:
        query += """
            AND (
                p.nome LIKE ?
                OR p.cpf LIKE ?
                OR CAST(s.id AS TEXT) LIKE ?
            )
        """

        parametros.extend([
            f"%{busca}%",
            f"%{busca}%",
            f"%{busca}%"
        ])

    if status:
        query += " AND s.status = ?"
        parametros.append(status)

    query += """
        GROUP BY s.id
        ORDER BY s.id DESC
    """

    solicitacoes = conexao.execute(
        query,
        parametros
    ).fetchall()

    conexao.close()

    return render_template(
        "situacao_exames.html",
        solicitacoes=solicitacoes
    )


@app.route("/perfil")
@login_required
def perfil():
    conexao = conectar()

    usuario = conexao.execute(
        """
        SELECT id, nome, email, perfil
        FROM usuarios
        WHERE id = ?
        """,
        (session["usuario_id"],)
    ).fetchone()

    conexao.close()

    return render_template(
        "perfil.html",
        usuario=usuario
    )


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
@login_required
def administracao():
    return render_template("dashboard_admin.html")


if __name__ == "__main__":
    app.run(debug=True)


