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

    # ===============================
    # TABELA UTILIZADORES (Autenticação)
    # ===============================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilizadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE,
        senha TEXT NOT NULL,
        perfil TEXT NOT NULL,
        telefone TEXT NOT NULL, 
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
    # Se a tabela já existia sem a coluna 'data_registo', este bloco força a sua criação
    try:
        cursor.execute("ALTER TABLE estudantes ADD COLUMN data_registo TEXT;")
    except sqlite3.OperationalError:
        # Se o erro for "duplicate column name", significa que a coluna já existe, podemos ignorar
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
        estado TEXT
    )
    """)

    # Se a tabela já existia antes sem a coluna 'tipo' ou 'estado', estes blocos evitam erros:
    try:
        cursor.execute("ALTER TABLE bolsas ADD COLUMN tipo TEXT;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE bolsas ADD COLUMN estado TEXT;")
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
    # 1. Administrador Padrão
    cursor.execute("""
    INSERT OR IGNORE INTO utilizadores (nome, email, senha, perfil, telefone, data_criacao)
    VALUES ('Benedita Samara Duarte Tavares', 'admin@sibes.com', '1234', 'Administrador', '9991122', DATE('now'))
    """)

    # 2. Secretária Padrão
    cursor.execute("""
    INSERT OR IGNORE INTO utilizadores (nome, email, senha, perfil, data_criacao)
    VALUES ('Secretária Geral', 'secretaria@sibes.com', '1234', 'Secretaria', DATE('now'))
    """)

    # 3. Um estudante de teste inicial
    cursor.execute("""
    INSERT OR IGNORE INTO utilizadores (nome, email, senha, perfil, data_criacao)
    VALUES ('Estudante Exemplo', 'estudante@sibes.com', '1234', 'Estudante', DATE('now'))
    """)
    
    
    conn.commit()
    conn.close()


def registar_novo_estudante(nome, email, senha, telefone="", universidade="", curso="", ano=1, media=0.0, rendimento=0.0):
    
    conn = conectar()
    cursor = conn.cursor()

    try:
        # 1. Inserir na tabela de utilizadores para permitir o login futuro
        cursor.execute("""
            INSERT INTO utilizadores (nome, email, senha, perfil, data_criacao)
            VALUES (?, ?, ?, 'Estudante', DATE('now'))
        """, (nome, email, senha))

        # 2. Inserir na tabela de estudantes com os detalhes específicos
        cursor.execute("""
            INSERT INTO estudantes (nome, email, telefone, universidade, curso, ano, media, rendimento, data_registo, data_criacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, DATE('now'), DATE('now'))
        """, (nome, email, telefone, universidade, curso, ano, media, rendimento))

        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Erro se o email já estiver registado na base de dados (chave UNIQUE)
        return False
    finally:
        conn.close()
        
def registar_nova_bolsa(nome, tipo, valor, estado):
    """Insere uma nova bolsa diretamente na base de dados"""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO bolsas (nome, tipo, valor, estado) 
            VALUES (?, ?, ?, ?)
        """, (nome, tipo, valor, estado))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao registar bolsa: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    criar_base()