import sqlite3
import os

DATABASE = "database/sibes.db"


def conectar():
    return sqlite3.connect(DATABASE)


def criar_base():
    # cria pasta se não existir
    os.makedirs("database", exist_ok=True)

    conn = conectar()
    cursor = conn.cursor()

    # ===============================
    # TABELA UTILIZADORES
    # ===============================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilizadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE,
        senha TEXT NOT NULL,
        perfil TEXT NOT NULL,
        data_criacao DATE
    )
    """)

    # ===============================
    # TABELA ESTUDANTES
    # ===============================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE,
        telefone TEXT,
        universidade TEXT,
        curso TEXT,
        ano INTEGER,
        media REAL,
        rendimento REAL,
        data_registo DATE,
        data_criacao DATE
    )
    """)

    # ===============================
    # TABELA BOLSAS
    # ===============================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bolsas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        tipo TEXT,
        valor REAL,
        vagas INTEGER,
        data_inicio DATE,
        data_fim DATE,
        estado TEXT
    )
    """)

    # ===============================
    # TABELA CANDIDATURAS
    # ===============================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidaturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estudante_id INTEGER,
        bolsa_id INTEGER,
        data_candidatura DATE,
        estado TEXT,
        observacoes TEXT,

        FOREIGN KEY(estudante_id) REFERENCES estudantes(id),
        FOREIGN KEY(bolsa_id) REFERENCES bolsas(id)
    )
    """)

    # ===============================
    # TABELA AVALIAÇÕES
    # ===============================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidatura_id INTEGER,
        media_academica REAL,
        rendimento_familiar REAL,
        pontuacao REAL,
        resultado TEXT,
        data_avaliacao DATE,

        FOREIGN KEY(candidatura_id) REFERENCES candidaturas(id)
    )
    """)

    # ===============================
    # TABELA RELATÓRIOS
    # ===============================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS relatorios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        data_geracao DATE
    )
    """)

    # ===============================
    # UTILIZADOR ADMIN PADRÃO
    # ===============================
    cursor.execute("""
    INSERT OR IGNORE INTO utilizadores
    (nome, email, senha, perfil, data_criacao)
    VALUES
    (
        'Administrador',
        'admin@sibes.com',
        '1234',
        'Administrador',
        DATE('now')
    )
    """)

def inserir_estudante(nome, email, telefone, universidade, curso, media, rendimento):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO estudantes
        (nome, email, telefone, universidade, curso, media, rendimento, data_registo, data_criacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, DATE('now'), DATE('now'))
    """, (nome, email, telefone, universidade, curso, media, rendimento))

    conn.commit()
    conn.close()
    


if __name__ == "__main__":
    criar_base()