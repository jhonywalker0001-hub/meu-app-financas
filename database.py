import sqlite3
import os
from kivy.utils import platform

def obter_caminho_banco():
    """
    Define o caminho correto do banco de dados dependendo da plataforma.
    No Android, usa a pasta de armazenamento interna do App.
    """
    nome_banco = "financas.db"
    
    if platform == 'android':
        from android.storage import app_storage_path
        caminho_pasta = app_storage_path()
        # Garante que estamos na pasta correta antes de criar o arquivo
        caminho_completo = os.path.join(caminho_pasta, nome_banco)
    else:
        # No PC (Windows/Linux), salva na pasta atual do projeto
        caminho_completo = nome_banco
        
    return caminho_completo

def conectar():
    """Retorna uma conexão com o banco de dados no caminho correto."""
    caminho = obter_caminho_banco()
    return sqlite3.connect(caminho)

def criar_tabela():
    """Cria a tabela de transações se ela não existir."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL NOT NULL,
            descricao TEXT NOT NULL,
            categoria TEXT,
            tipo TEXT NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def criar_tabela_metas():
    """Cria a tabela de metas se ela não existir."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor_objetivo REAL NOT NULL,
            valor_poupado REAL DEFAULT 0,
            data_limite TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Exemplo de função para salvar (insira conforme sua lógica de campos)
def salvar_transacao(valor, descricao, categoria, tipo, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transacoes (valor, descricao, categoria, tipo, data)
        VALUES (?, ?, ?, ?, ?)
    ''', (valor, descricao, categoria, tipo, data))
    conn.commit()
    conn.close()
