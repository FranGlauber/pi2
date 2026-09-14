from app import app
from flask import request, render_template, redirect, session, url_for
from models.paciente_model import *
#from auth import login_required

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# rotas
@app.route("/paciente/novo")
def inserir_paciente():
 return render_template("pacientes.html")

@app.route("/paciente/create", methods=['POST'])
#@login_required
def criar_paciente():
 if request.method == 'POST':
 # Captura os dados enviados pelo formulário
    cpf = request.form['cpf']
    nome = request.form['nome']
    data = request.form['data']
    sexo = request.form['sexo']
    telefone = request.form['telefone']
    email = request.form['email']
    cep = request.form['cep']
    endereco = request.form['endereco']
    cidade = request.form['cidade']
    obs = request.form['obs']

 # Cria um novo paciente
 new_paciente = Paciente(cpf=cpf, nome=nome, data=data, sexo=sexo, telefone=telefone,
                          email=email, cep=cep, endereco=endereco, cidade=cidade, obs=obs)

 # Cria um novo paciente no banco de dados
 db = SessionLocal()

 # Adiciona o novo paciente ao banco de dados
 db.add(new_paciente)
 db.commit()
 return render_template('pacientes.html', pacientes=db.query(Paciente).all())

@app.route("/paciente/lista")
#@login_required
def listar_pacientes():
    db = SessionLocal()
    # Consultar todos os pacientes
    pacientes = db.query(Paciente).all()
    # Renderizar o HTML passando os dados
    return render_template('pacientes.html', pacientes=pacientes)

@app.route('/paciente/deletar/<int:item_id>')
#@login_required
def deletar_paciente(item_id):
    db = SessionLocal()
    item = db.query(Paciente).get(item_id) # Busca o item pelo id
    if item:
        db.delete(item) # Deleta o item
        db.commit()
    return render_template('pacientes.html', pacientes=db.query(Paciente).all())

@app.route("/paciente/editar/<int:id>")
#@login_required
def editar_paciente(id):
    db = SessionLocal()
    paciente = db.query(Paciente).filter(Paciente.id == id).first()
    return render_template("paciente/atualizar.html", paciente=paciente)

@app.route("/paciente/editar", methods=["POST"])
#@login_required
def editar_paciente_salvar():
        db = SessionLocal()
        id = request.form.get("id")
        cpf = request.form.get("cpf")
        nome = request.form.get("nome")
        data = request.form.get("data")
        sexo = request.form.get("sexo")
        telefone = request.form.get("telefone")
        email = request.form.get("email")
        cep = request.form.get("cep")
        endereco = request.form.get("endereco")
        cidade = request.form.get("cidade")
        obs = request.form.get("obs")
        paciente = db.query(Paciente).filter(Paciente.id == id).first()
        paciente.cpf = cpf
        paciente.nome = nome
        paciente.data = data
        paciente.sexo = sexo
        paciente.telefone = telefone
        paciente.email = email
        paciente.cep = cep
        paciente.endereco = endereco
        paciente.cidade = cidade
        paciente.obs = obs

        db.commit()
        return render_template("pacientes.html", pacientes=db.query(Paciente).all())


