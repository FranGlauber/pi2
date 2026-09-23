from models.conexao import *

class Funcionarios(Base):
 __tablename__ = "funcionarios"
 id = Column("id", Integer, primary_key=True, autoincrement=True)
 cpf = Column("cpf", String(15))
 nome = Column("nome", String(200))
 data = Column("data", String(10))
 sexo = Column("sexo", String(10))
 telefone = Column("telefone", String(15))
 email = Column("email", String(100))
 senha = Column("senha", String(10))
 endereco = Column("endereco", String(200))
 cidade = Column("cidade", String(100))
 cargo = Column("cargo", String(200))

 
 def __init__(self, cpf, nome, data, sexo, telefone, email, senha, endereco, cidade, cargo):
    self.cpf = cpf
    self.nome = nome
    self.data = data
    self.sexo = sexo
    self.telefone = telefone
    self.email = email
    self.senha = senha
    self.endereco = endereco
    self.cidade = cidade
    self.cargo = cargo