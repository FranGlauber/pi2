import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "laboratorio.db"


def conectar():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_banco():
    conexao = conectar()

    conexao.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            data_nascimento TEXT NOT NULL,
            sexo TEXT NOT NULL,
            telefone TEXT,
            email TEXT,
            cep TEXT,
            endereco TEXT,
            numero TEXT,
            complemento TEXT,
            bairro TEXT,
            cidade TEXT,
            estado TEXT,
            criado_em TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tipos_exames (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT
        );

        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            data_solicitacao TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Aguardando coleta',
            observacoes TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );

        CREATE TABLE IF NOT EXISTS solicitacao_exames (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            solicitacao_id INTEGER NOT NULL,
            exame_id INTEGER NOT NULL,
            FOREIGN KEY (solicitacao_id) REFERENCES solicitacoes(id),
            FOREIGN KEY (exame_id) REFERENCES tipos_exames(id)
        );

        CREATE TABLE IF NOT EXISTS coletas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            solicitacao_id INTEGER NOT NULL UNIQUE,
            tecnico_id INTEGER,
            data_coleta TEXT,
            horario TEXT,
            material TEXT,
            observacoes TEXT,
            FOREIGN KEY (solicitacao_id) REFERENCES solicitacoes(id),
            FOREIGN KEY (tecnico_id) REFERENCES usuarios(id)
        );

        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            solicitacao_exame_id INTEGER NOT NULL UNIQUE,
            analista_id INTEGER,
            resultado TEXT,
            observacoes TEXT,
            parecer TEXT,
            data_resultado TEXT,
            validado INTEGER DEFAULT 0,
            FOREIGN KEY (solicitacao_exame_id) REFERENCES solicitacao_exames(id),
            FOREIGN KEY (analista_id) REFERENCES usuarios(id)
        );
    """)

    usuario = conexao.execute(
        "SELECT id FROM usuarios WHERE email = ?",
        ("recepcao@laboratorio.com",)
    ).fetchone()

    if usuario is None:
        conexao.execute(
            """
            INSERT INTO usuarios (nome, email, senha, perfil)
            VALUES (?, ?, ?, ?)
            """,
            (
                "Recepcionista",
                "recepcao@laboratorio.com",
                "123456",
                "recepcionista"
            )
        )

    exames = [
        ("Hemograma", "Análise das células do sangue"),
        ("Glicemia", "Medição da glicose no sangue"),
        ("Colesterol Total", "Avaliação do colesterol total"),
        ("Triglicerídeos", "Avaliação dos triglicerídeos"),
        ("TSH", "Avaliação do hormônio estimulante da tireoide"),
        ("T4 Livre", "Avaliação da tiroxina livre"),
        ("Urina Tipo 1", "Análise de urina")
    ]

    for nome, descricao in exames:
        conexao.execute(
            """
            INSERT OR IGNORE INTO tipos_exames (nome, descricao)
            VALUES (?, ?)
            """,
            (nome, descricao)
        )

    conexao.commit()
    conexao.close()
