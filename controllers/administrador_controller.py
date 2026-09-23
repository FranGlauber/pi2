from app import app
from flask import request, render_template, redirect, session, url_for
from models.administrador_model import *
#from auth import login_required

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# rotas
@app.route("/funcionario/novo")
def inserir_funcionario():
 return render_template("funcionarios.html")

@app.route("/funcionario/create", methods=['POST'])
#@login_required
def criar_funcionario():
 if request.method == 'POST':
 # Captura os dados enviados pelo formulário
    cpf = request.form['cpf']
    nome = request.form['nome']
    data = request.form['data']
    sexo = request.form['sexo']
    telefone = request.form['telefone']
    email = request.form['email']
    senha = request.form['senha']
    endereco = request.form['endereco']
    cidade = request.form['cidade']
    cargo = request.form['cargo']

 # Cria um novo funcionário
 new_funcionario = Funcionarios(cpf=cpf, nome=nome, data=data, sexo=sexo, telefone=telefone,
                                    email=email, senha=senha, endereco=endereco, cidade=cidade, cargo=cargo)

 # Cria um novo funcionário no banco de dados
 db = SessionLocal()

 # Adiciona o novo funcionário ao banco de dados
 db.add(new_funcionario)
 db.commit()
 return render_template('funcionarios.html', funcionarios=db.query(Funcionarios).all())

@app.route("/funcionario/lista")
#@login_required
def listar_funcionarios():
    db = SessionLocal()
    # Consultar todos os funcionários
    funcionarios = db.query(Funcionarios).all()
    # Renderizar o HTML passando os dados
    return render_template('funcionarios.html', funcionarios=funcionarios)

@app.route('/funcionario/deletar/<int:item_id>')
#@login_required
def deletar_funcionario(item_id):
    db = SessionLocal()
    item = db.query(Funcionarios).get(item_id) # Busca o item pelo id
    if item:
        db.delete(item) # Deleta o item
        db.commit()
    return render_template('funcionarios.html', funcionarios=db.query(Funcionarios).all())

@app.route("/funcionario/editar/<int:id>")
#@login_required
def editar_funcionario(id):
    db = SessionLocal()
    funcionarios = db.query(Funcionarios).filter(Funcionarios.id == id).first()
    return render_template("funcionario/atualizar.html", funcionario=funcionarios)

@app.route("/funcionario/editar", methods=["POST"])
#@login_required
def editar_funcionario_salvar():
        db = SessionLocal()
        id = request.form.get("id")
        cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        data = request.form.get("data")
        sexo = request.form.get("sexo")
        telefone = request.form.get("telefone")
        email = request.form.get("email")
        senha = request.form.get("senha")
        endereco = request.form.get("endereco")
        cidade = request.form.get("cidade")
        cargo = request.form.get("cargo")
        funcionarios = db.query(Funcionarios).filter(Funcionarios.id == id).first()
        funcionarios.cpf = cpf
        funcionarios.nome = nome
        funcionarios.data = data
        funcionarios.sexo = sexo
        funcionarios.telefone = telefone
        funcionarios.email = email
        funcionarios.senha = senha
        funcionarios.endereco = endereco
        funcionarios.cidade = cidade
        funcionarios.cargo = cargo

        db.commit()
        return render_template("funcionarios.html", funcionarios=db.query(Funcionarios).all())


