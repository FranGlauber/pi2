"""
Cria (ou atualiza) um usuário administrador para testar o sistema.

Como usar (na raiz do projeto, onde fica o main.py):
    python criar_admin.py
"""
from datetime import date

from sqlalchemy import Date
from werkzeug.security import generate_password_hash

from models.conexao import Base, Session, engine
from models.administrador_model import Funcionarios

# ---- DADOS DO ADMIN DE TESTE (pode alterar) ----
EMAIL = "admin@teste.com"
SENHA = "admin123"
# -------------------------------------------------

# Garante que as tabelas existem
Base.metadata.create_all(engine)

# Se a coluna "data" for do tipo Date, usa um objeto date; senão, texto
if isinstance(Funcionarios.data.type, Date):
    data_nasc = date(1990, 1, 1)
else:
    data_nasc = "1990-01-01"

with Session() as db:
    admin = db.query(Funcionarios).filter(Funcionarios.email == EMAIL).first()

    if admin:
        # Já existe: apenas redefine senha e cargo
        admin.senha = generate_password_hash(SENHA)
        admin.cargo = "administrador"
        db.commit()
        print(f"Administrador já existia. Senha redefinida para '{SENHA}'.")
    else:
        admin = Funcionarios(
            cpf="00000000000",
            nome="Administrador",
            data=data_nasc,
            sexo="M",
            telefone="00000000000",
            email=EMAIL,
            senha=generate_password_hash(SENHA),
            endereco="Endereço de teste",
            cidade="Sobral",
            cargo="administrador",
        )
        db.add(admin)
        db.commit()
        print("Administrador criado com sucesso!")

print(f"\nLogin:  {EMAIL}")
print(f"Senha:  {SENHA}")