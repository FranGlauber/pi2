"""
Cria (ou atualiza) usuários de teste para cada cargo do sistema:
administrador, analista, tecnico e recepcionista.

Como usar (na raiz do projeto, onde fica o main.py):
    python criar_usuarios.py
"""
from datetime import date

from sqlalchemy import Date
from werkzeug.security import generate_password_hash

from models.conexao import Base, Session, engine
from models.administrador_model import Funcionarios

# ---- USUÁRIOS DE TESTE (pode alterar) ----
# O "cargo" deve ser igual ao usado no DASHBOARD_POR_CARGO do main.py
USUARIOS = [
    {
        "nome": "Administrador",
        "email": "admin@teste.com",
        "senha": "admin123",
        "cargo": "administrador",
        "cpf": "00000000001",
    },
    {
        "nome": "Analista",
        "email": "analista@teste.com",
        "senha": "analista123",
        "cargo": "analista",
        "cpf": "00000000002",
    },
    {
        "nome": "Técnico",
        "email": "tecnico@teste.com",
        "senha": "tecnico123",
        "cargo": "tecnico",
        "cpf": "00000000003",
    },
    {
        "nome": "Recepcionista",
        "email": "recepcionista@teste.com",
        "senha": "recepcionista123",
        "cargo": "recepcionista",
        "cpf": "00000000004",
    },
]
# -------------------------------------------

# Garante que as tabelas existem
Base.metadata.create_all(engine)

# Se a coluna "data" for do tipo Date, usa um objeto date; senão, texto
if isinstance(Funcionarios.data.type, Date):
    data_nasc = date(1990, 1, 1)
else:
    data_nasc = "1990-01-01"

with Session() as db:
    for u in USUARIOS:
        existente = (
            db.query(Funcionarios).filter(Funcionarios.email == u["email"]).first()
        )

        if existente:
            # Já existe: apenas redefine senha e cargo
            existente.senha = generate_password_hash(u["senha"])
            existente.cargo = u["cargo"]
            print(f"[atualizado] {u['cargo']:<14} {u['email']}")
        else:
            novo = Funcionarios(
                cpf=u["cpf"],
                nome=u["nome"],
                data=data_nasc,
                sexo="M",
                telefone="00000000000",
                email=u["email"],
                senha=generate_password_hash(u["senha"]),
                endereco="Endereço de teste",
                cidade="Sobral",
                cargo=u["cargo"],
            )
            db.add(novo)
            print(f"[criado]     {u['cargo']:<14} {u['email']}")

    db.commit()

print("\nLogins de teste:")
for u in USUARIOS:
    print(f"  {u['cargo']:<14} {u['email']:<26} senha: {u['senha']}")
