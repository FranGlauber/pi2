from models.conexao import Base, engine

# Importa todos os models
from models.paciente_model import Paciente
from models.administrador_model import Funcionarios

# Cria as tabelas
Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")