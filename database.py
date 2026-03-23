import sqlite3
import os

def conectar():
    """Estabelece conexão com o banco de dados financas.db"""
    # O arquivo será criado no diretório atual (definido pelo main.py no Android)
    return sqlite3.connect('financas.db')

def criar_tabela():
    """Cria a tabela de transações se não existir"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            data TEXT NOT NULL,
            descricao TEXT
        )
    ''')
    conn.commit()
    conn.close()

def criar_tabela_metas():
    """Cria a tabela de metas financeiras se não existir"""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor_objetivo REAL NOT NULL,
            valor_poupado REAL DEFAULT 0,
            data_limite TEXT,
            status TEXT DEFAULT 'Em andamento'
        )
    ''')
    conn.commit()
    conn.close()

# Funções auxiliares para facilitar o uso no app
def adicionar_transacao(tipo, valor, categoria, data, descricao=""):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transacoes (tipo, valor, categoria, data, descricao)
        VALUES (?, ?, ?, ?, ?)
    ''', (tipo, valor, categoria, data, descricao))
    conn.commit()
    conn.close()

def adicionar_meta(nome, valor_objetivo, data_limite):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO metas (nome, valor_objetivo, data_limite)
        VALUES (?, ?, ?)
    ''', (nome, valor_objetivo, data_limite))
    conn.commit()
    conn.close()
