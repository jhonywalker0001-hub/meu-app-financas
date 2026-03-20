import sqlite3
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import os
from kivy.utils import platform

def conectar():
    nome_db = "financas.db"
    if platform == 'android':
        from android.storage import app_storage_path
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

def calcular_saldo():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        SUM(CASE WHEN tipo='receita' THEN valor ELSE 0 END),
        SUM(CASE WHEN tipo='despesa' THEN valor ELSE 0 END)
    FROM transacoes
    """)
    res = cursor.fetchone()
    conn.close()
    receitas = res[0] or 0
    despesas = res[1] or 0
    return receitas - despesas

def adicionar_transacao(tipo, valor, descricao, categoria="Geral", data=None):
    if not data:
        data = datetime.now().strftime("%d/%m/%Y")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO transacoes (tipo, valor, descricao, categoria, data)
    VALUES (?, ?, ?, ?, ?)
    """, (tipo.lower(), valor, descricao, categoria, data))
    conn.commit()
    conn.close()

def listar_transacoes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes ORDER BY id DESC")
    colunas = [c[0] for c in cursor.description]
    dados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    conn.close()
    return dados

def resumo_transacoes():
    mes_atual = datetime.now().strftime("%m/%Y")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        SUM(CASE WHEN tipo='receita' THEN valor ELSE 0 END),
        SUM(CASE WHEN tipo='despesa' THEN valor ELSE 0 END)
    FROM transacoes
    WHERE data LIKE ?
    """, (f'%{mes_atual}',))
    res = cursor.fetchone()
    conn.close()
    return (res[0] or 0), (res[1] or 0)

def definir_meta(categoria, valor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO metas (categoria, valor_limite) VALUES (?, ?)
    ON CONFLICT(categoria) DO UPDATE SET valor_limite=excluded.valor_limite
    """, (categoria, valor))
    conn.commit()
    conn.close()

def obter_metas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT categoria, valor_limite FROM metas")
    dados = cursor.fetchall()
    conn.close()
    return {categoria: valor for categoria, valor in dados}

def obter_caminho_exportacao(nome_arquivo):
    if platform == 'android':
        from android.storage import primary_external_storage_path
        downloads_path = os.path.join(primary_external_storage_path(), 'Download')
        if not os.path.exists(downloads_path):
            os.makedirs(downloads_path)
        return os.path.join(downloads_path, nome_arquivo)
    return nome_arquivo

def exportar_para_excel(nome_arquivo, mes_filtro=None):
    caminho = obter_caminho_exportacao(nome_arquivo)
    conn = conectar()
    query = "SELECT data, categoria, descricao, tipo, valor FROM transacoes"
    df = pd.read_sql_query(query, conn)
    conn.close()
    df.to_excel(caminho, index=False)

def exportar_para_pdf(nome_arquivo, mes_filtro=None):
    caminho = obter_caminho_exportacao(nome_arquivo)
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT data, categoria, descricao, tipo, valor FROM transacoes")
    dados = cursor.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(190, 10, "Relatorio Financeiro", ln=True, align="C")
    # ... (lógica de exportação)
    pdf.output(caminho)

def deletar_transacao(id_transacao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacoes WHERE id = ?", (id_transacao,))
    conn.commit()
    conn.close()

def atualizar_transacao(id_transacao, tipo, valor, descricao, categoria, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE transacoes SET tipo=?, valor=?, descricao=?, categoria=?, data=? WHERE id=?
    """, (tipo.lower(), valor, descricao, categoria, data, id_transacao))
    conn.commit()
    conn.close()

# FUNÇÃO QUE RESOLVE O ERRO DE IMPORTAÇÃO
def limpar_banco_dados():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacoes")
    conn.commit()
    conn.close()