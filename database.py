import sqlite3
import os
from kivy.utils import platform

def obter_caminho_banco():
    """Define o caminho correto do banco de dados dependendo da plataforma."""
    nome_banco = "financas.db"
    
    if platform == 'android':
        from android.storage import app_storage_path
        caminho_pasta = app_storage_path()
        caminho_completo = os.path.join(caminho_pasta, nome_banco)
    else:
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

def salvar_transacao(valor, descricao, categoria, tipo, data):
    """Salva uma nova transação no banco."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transacoes (valor, descricao, categoria, tipo, data)
        VALUES (?, ?, ?, ?, ?)
    ''', (valor, descricao, categoria, tipo, data))
    conn.commit()
    conn.close()

# --- NOVAS FUNÇÕES PARA O DASHBOARD ---

def calcular_saldo():
    """Calcula o saldo total (Receitas - Despesas)."""
    conn = conectar()
    cursor = conn.cursor()
    # Soma receitas
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'receita'")
    receitas = cursor.fetchone()[0] or 0
    # Soma despesas
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'despesa'")
    despesas = cursor.fetchone()[0] or 0
    conn.close()
    return receitas - despesas

def resumo_transacoes():
    """Retorna o total de receitas e o total de despesas separadamente."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'receita'")
    rec = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'despesa'")
    desp = cursor.fetchone()[0] or 0
    conn.close()
    return rec, desp

def listar_transacoes():
    """Retorna todas as transações formatadas em uma lista de dicionários."""
    conn = conectar()
    conn.row_factory = sqlite3.Row # Permite acessar colunas pelo nome
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes ORDER BY data DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def deletar_transacao(id_t):
    """Remove uma transação específica pelo ID."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacoes WHERE id = ?", (id_t,))
    conn.commit()
    conn.close()
