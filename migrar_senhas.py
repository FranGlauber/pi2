from models.conexao import Session
from models.administrador_model import Funcionarios
from werkzeug.security import generate_password_hash

with Session() as db:
    for f in db.query(Funcionarios).all():
        # Evita fazer hash de hash caso rode duas vezes
        if not f.senha.startswith(("scrypt:", "pbkdf2:")):
            f.senha = generate_password_hash(f.senha)
    db.commit()

print("Senhas convertidas com sucesso.")