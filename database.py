import sqlite3
import os
from kivy.utils import platform

def obter_caminho_banco():
    """Define o caminho correto do banco de dados dependendo da plataforma."""
    nome_banco = "financas.db"
    
    if platform == 'android':
        from android.storage import app_storage_path
        caminho_pasta = app_storage_path()
        # Garante o uso do caminho absoluto no Android para evitar banco vazio
        caminho_completo = os.path.join(caminho_pasta, nome_banco)
    else:
        # No PC (Windows/Linux), salva na pasta atual do projeto
        caminho_completo = nome_banco
        
    return caminho_completo

def conectar():
    """Retorna uma conexão com o banco de dados no caminho correto."""
    caminho = obter_caminho_banco()
    return sqlite3.connect(caminho)

# --- CRIAÇÃO DE TABELAS ---

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

# --- FUNÇÕES DE TRANSAÇÕES ---

def salvar_transacao(valor, descricao, categoria, tipo, data):
    """Salva uma nova transação no banco."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transacoes (valor, descricao, categoria, tipo, data)
        VALUES (?, ?, ?, ?, ?)
    ''', (valor, descricao, categoria, tipo.lower(), data))
    conn.commit()
    conn.close()

def calcular_saldo():
    """Calcula o saldo total (Receitas - Despesas)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'receita'")
    receitas = cursor.fetchone()[0] or 0
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
    conn.row_factory = sqlite3.Row 
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

# --- FUNÇÕES DE METAS ---

def definir_meta(categoria, limite):
    """Salva ou atualiza o limite de gasto para uma categoria."""
    conn = conectar()
    cursor = conn.cursor()
    # Verifica se já existe meta para a categoria
    cursor.execute("SELECT id FROM metas WHERE nome = ?", (categoria,))
    existe = cursor.fetchone()
    
    if existe:
        cursor.execute("UPDATE metas SET valor_objetivo = ? WHERE nome = ?", (limite, categoria))
    else:
        cursor.execute("INSERT INTO metas (nome, valor_objetivo) VALUES (?, ?)", (categoria, limite))
    
    conn.commit()
    conn.close()

def obter_metas():
    """Retorna um dicionário com {categoria: limite} para a tela de Metas."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, valor_objetivo FROM metas")
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}
