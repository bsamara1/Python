import sqlite3
import os

# 1. Encontra a pasta onde este próprio ficheiro 'database.py' está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Garante que o sibes.db aponta SEMPRE para o sítio correto (dentro dessa pasta)
DATABASE = os.path.join(BASE_DIR, "sibes.db")

def conectar():
    """Estabelece a ligação com a base de dados SQLite usando um caminho absoluto."""
    return sqlite3.connect(DATABASE)

def criar_base():
    """Cria a pasta e todas as tabelas necessárias se não existirem."""
    # Cria a pasta se não existir
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    conn = conectar()
    cursor = conn.cursor()

    # ==========================================================
    # TABELA UTILIZADORES (Autenticação)
    # CORREÇÃO: 'telefone' agora aceita NULL para evitar erros no registo inicial
    # ==========================================================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilizadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE,
        senha TEXT NOT NULL,
        perfil TEXT NOT NULL,
        telefone TEXT, 
        data_criacao DATE
    )
    """)

    # ===============================
    # TABELA ESTUDANTES (Dados Académicos)
    # ===============================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        telefone TEXT,
        universidade TEXT,
        curso TEXT,
        ano INTEGER,
        media REAL,
        rendimento REAL,
        data_registo TEXT,
        data_criacao TEXT
    );
    """)

    # --- CORREÇÃO AUTOMÁTICA PARA BASES DE DADOS ANTIGAS ---
    try:
        cursor.execute("ALTER TABLE estudantes ADD COLUMN data_registo TEXT;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE estudantes ADD COLUMN data_criacao TEXT;")
    except sqlite3.OperationalError:
        pass
    # --------------------------------------------------------

    # ===============================
    # TABELA BOLSAS
    # ===============================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bolsas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        tipo TEXT,
        valor REAL,
        estado TEXT,
        media_minima REAL DEFAULT 0.0,
        rendimento_maximo REAL DEFAULT 999999.0
    )
    """)
    # No final da função criar_base(), mude a lógica para:

    # Verifica se já existem bolsas cadastradas
    cursor.execute("SELECT COUNT(*) FROM bolsas")
    se_vazio = cursor.fetchone()[0] == 0

    if se_vazio:
        # Se a tabela estiver limpa, insere os exemplos
        cursor.execute("""
        INSERT INTO bolsas (nome, tipo, valor, estado, media_minima, rendimento_maximo)
        VALUES ('Bolsa de Mérito', 'Mérito', 5000, 'Ativo', 15.0, 999999)
        """)

        cursor.execute("""
        INSERT INTO bolsas (nome, tipo, valor, estado, media_minima, rendimento_maximo)
        VALUES ('Bolsa Social', 'Social', 3000, 'Ativo', 10.0, 35000)
        """)

        cursor.execute("""
        INSERT INTO bolsas (nome, tipo, valor, estado, media_minima, rendimento_maximo)
        VALUES ('Bolsa de Estudo Integral', 'Integral', 8000, 'Ativo', 16.0, 45000)
        """)

    # Migrations para compatibilidade com bases antigas
    try:
        cursor.execute("ALTER TABLE bolsas ADD COLUMN tipo TEXT;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE bolsas ADD COLUMN estado TEXT;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE bolsas ADD COLUMN media_minima REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE bolsas ADD COLUMN rendimento_maximo REAL DEFAULT 999999.0;")
    except sqlite3.OperationalError:
        pass

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

    # ==================================================
    # UTILIZADORES PADRÃO (Para os primeiros testes)
    # ==================================================
    cursor.execute("""
    INSERT OR IGNORE INTO utilizadores (nome, email, senha, perfil, telefone, data_criacao)
    VALUES ('Benedita Samara Duarte Tavares', 'admin@sibes.com', '1234', 'Administrador', '9991122', DATE('now'))
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO utilizadores (nome, email, senha, perfil, data_criacao)
    VALUES ('Secretária Geral', 'secretaria@sibes.com', '1234', 'Secretaria', DATE('now'))
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO utilizadores (nome, email, senha, perfil, data_criacao)
    VALUES ('Estudante Exemplo', 'estudante@sibes.com', '1234', 'Estudante', DATE('now'))
    """)

    # ==================================================
    # BOLSAS DE EXEMPLO (Com novos campos)
    # ==================================================
    cursor.execute("""
    INSERT OR IGNORE INTO bolsas (nome, tipo, valor, estado, media_minima, rendimento_maximo)
    VALUES ('Bolsa de Mérito', 'Mérito', 5000, 'Ativo', 15.0, 999999)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO bolsas (nome, tipo, valor, estado, media_minima, rendimento_maximo)
    VALUES ('Bolsa Social', 'Social', 3000, 'Ativo', 10.0, 35000)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO bolsas (nome, tipo, valor, estado, media_minima, rendimento_maximo)
    VALUES ('Bolsa de Estudo Integral', 'Integral', 8000, 'Ativo', 16.0, 45000)
    """)

    conn.commit()
    conn.close()


def registar_novo_estudante(nome, email, senha, telefone="", universidade="", curso="", ano=1, media=0.0, rendimento=0.0):
    conn = conectar()
    cursor = conn.cursor()

    try:
        # 1. Inserir na tabela de utilizadores (agora passando também a variável telefone)
        cursor.execute("""
            INSERT INTO utilizadores (nome, email, senha, perfil, telefone, data_criacao)
            VALUES (?, ?, ?, 'Estudante', ?, DATE('now'))
        """, (nome, email, senha, telefone))

        # 2. Inserir na tabela de estudantes com os detalhes específicos
        cursor.execute("""
            INSERT INTO estudantes (nome, email, telefone, universidade, curso, ano, media, rendimento, data_registo, data_criacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, DATE('now'), DATE('now'))
        """, (nome, email, telefone, universidade, curso, ano, media, rendimento))

        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        # Mostra o erro real no terminal para debug
        print(f"Erro de integridade no SQLite: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Erro no SQLite: {e}")
        return False
    finally:
        conn.close()
        
def registar_nova_bolsa(nome, tipo, valor, estado, media_minima=0.0, rendimento_maximo=999999.0):
    """Insere uma nova bolsa diretamente na base de dados"""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO bolsas (nome, tipo, valor, estado, media_minima, rendimento_maximo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, tipo, valor, estado, media_minima, rendimento_maximo))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao registar bolsa: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    criar_base()