from models.conexao import *

class Paciente(Base):
 __tablename__ = "pacientes"
 id = Column("id", Integer, primary_key=True, autoincrement=True)
 cpf = Column("cpf", String(15))
 nome = Column("nome", String(200))
 data = Column("data", String(10))
 sexo = Column("sexo", String(10))
 telefone = Column("telefone", String(15))
 email = Column("email", String(100))
 cep = Column("cep", String(10))
 endereco = Column("endereco", String(200))
 cidade = Column("cidade", String(100))
 obs = Column("obs", String(200))

 
 def __init__(self, cpf, nome, data, sexo, telefone, email, cep, endereco, cidade, obs):
    self.cpf = cpf
    self.nome = nome
    self.data = data
    self.sexo = sexo
    self.telefone = telefone
    self.email = email
    self.cep = cep
    self.endereco = endereco
    self.cidade = cidade
    self.obs = obs