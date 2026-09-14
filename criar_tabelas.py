from models.conexao import Base, engine


# Cria as tabelas
Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")