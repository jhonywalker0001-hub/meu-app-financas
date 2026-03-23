import sqlite3
import pandas as pd
from datetime import datetime
import os
from kivy.utils import platform

# Usaremos fpdf2 que é mais atualizada para Android
try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

def conectar():
    nome_db = "financas.db"
    if platform == 'android':
        from android.storage import app_storage_path
        # No Android, o banco fica na pasta privada do app
        caminho = os.path.join(app_storage_path(), nome_db)
    else:
        caminho = nome_db
    return sqlite3.connect(caminho, check_same_thread=False)

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT, valor REAL, descricao TEXT, categoria TEXT, data TEXT
    )""")
    # Tenta adicionar a coluna categoria se ela não existir (migração)
    try:
        cursor.execute("ALTER TABLE transacoes ADD COLUMN categoria TEXT")
    except:
        pass
    conn.commit()
    conn.close()

def criar_tabela_metas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT UNIQUE, valor_limite REAL
    )""")
    conn.commit()
    conn.close()

def obter_caminho_exportacao(nome_arquivo):
    if platform == 'android':
        # Tenta salvar na pasta de documentos do app para evitar erro de permissão do Android 13
        from android.storage import app_storage_path
        caminho_base = app_storage_path()
        return os.path.join(caminho_base, nome_arquivo)
    return nome_arquivo

def exportar_para_excel(nome_arquivo, mes_filtro=None):
    caminho = obter_caminho_exportacao(nome_arquivo)
    conn = conectar()
    query = "SELECT data, categoria, descricao, tipo, valor FROM transacoes"
    df = pd.read_sql_query(query, conn)
    conn.close()
    df.to_excel(caminho, index=False)
    return caminho # Retorna o caminho para avisar o usuário

# ... (restante das funções de cálculo permanecem iguais, apenas sem espaços invisíveis)

def calcular_saldo():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(CASE WHEN tipo='receita' THEN valor ELSE 0 END), SUM(CASE WHEN tipo='despesa' THEN valor ELSE 0 END) FROM transacoes")
    res = cursor.fetchone()
    conn.close()
    receitas = res[0] or 0
    despesas = res[1] or 0
    return receitas - despesas
