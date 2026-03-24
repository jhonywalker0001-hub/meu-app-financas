import sqlite3
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import os
from kivy.utils import platform

def conectar():
    nome_db = "financas.db"
    # Lógica original para garantir que o banco seja salvo no local correto no Android
    if platform == 'android':
        from android.storage import app_storage_path
        caminho = os.path.join(app_storage_path(), nome_db)
    else:
        caminho = nome_db
    return sqlite3.connect(caminho, check_same_thread=False)

def criar_tabela():
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT, 
            valor REAL, 
            descricao TEXT, 
            categoria TEXT, 
            data TEXT
        )""")
        # Mantendo sua lógica de migração de coluna categoria
        try:
            cursor.execute("ALTER TABLE transacoes ADD COLUMN categoria TEXT")
        except:
            pass
        conn.commit()
    finally:
        conn.close()

def criar_tabela_metas():
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT UNIQUE, 
            valor_limite REAL
        )""")
        conn.commit()
    finally:
        conn.close()

def calcular_saldo():
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT 
            SUM(CASE WHEN tipo='receita' THEN valor ELSE 0 END),
            SUM(CASE WHEN tipo='despesa' THEN valor ELSE 0 END)
        FROM transacoes
        """)
        res = cursor.fetchone()
        receitas = res[0] or 0
        despesas = res[1] or 0
        return receitas - despesas
    finally:
        conn.close()

def adicionar_transacao(tipo, valor, descricao, categoria="Geral", data=None):
    if not data:
        data = datetime.now().strftime("%d/%m/%Y")
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO transacoes (tipo, valor, descricao, categoria, data)
        VALUES (?, ?, ?, ?, ?)
        """, (tipo.lower(), valor, descricao, categoria, data))
        conn.commit()
    finally:
        conn.close()

def listar_transacoes():
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transacoes ORDER BY id DESC")
        colunas = [c[0] for c in cursor.description]
        dados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        return dados
    finally:
        conn.close()

def resumo_transacoes():
    mes_atual = datetime.now().strftime("%m/%Y")
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT 
            SUM(CASE WHEN tipo='receita' THEN valor ELSE 0 END),
            SUM(CASE WHEN tipo='despesa' THEN valor ELSE 0 END)
        FROM transacoes
        WHERE data LIKE ?
        """, (f'%{mes_atual}',))
        res = cursor.fetchone()
        return (res[0] or 0), (res[1] or 0)
    finally:
        conn.close()

def definir_meta(categoria, valor):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO metas (categoria, valor_limite) VALUES (?, ?)
        ON CONFLICT(categoria) DO UPDATE SET valor_limite=excluded.valor_limite
        """, (categoria, valor))
        conn.commit()
    finally:
        conn.close()

def obter_metas():
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT categoria, valor_limite FROM metas")
        dados = cursor.fetchall()
        return {categoria: valor for categoria, valor in dados}
    finally:
        conn.close()

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
    try:
        query = "SELECT data, categoria, descricao, tipo, valor FROM transacoes"
        df = pd.read_sql_query(query, conn)
        df.to_excel(caminho, index=False)
    finally:
        conn.close()

def exportar_para_pdf(nome_arquivo, mes_filtro=None):
    caminho = obter_caminho_exportacao(nome_arquivo)
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT data, categoria, descricao, tipo, valor FROM transacoes")
        dados = cursor.fetchall()
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(190, 10, "Relatorio Financeiro", ln=True, align="C")
        
        # Cabeçalho da tabela
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(30, 10, "Data", 1)
        pdf.cell(40, 10, "Categoria", 1)
        pdf.cell(60, 10, "Descricao", 1)
        pdf.cell(30, 10, "Tipo", 1)
        pdf.cell(30, 10, "Valor", 1, ln=True)

        # Dados
        pdf.set_font("Helvetica", "", 10)
        for row in dados:
            pdf.cell(30, 10, str(row[0]), 1)
            pdf.cell(40, 10, str(row[1]), 1)
            pdf.cell(60, 10, str(row[2]), 1)
            pdf.cell(30, 10, str(row[3]), 1)
            pdf.cell(30, 10, f"R$ {row[4]:.2f}", 1, ln=True)

        pdf.output(caminho)
    finally:
        conn.close()

def deletar_transacao(id_transacao):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transacoes WHERE id = ?", (id_transacao,))
        conn.commit()
    finally:
        conn.close()

def atualizar_transacao(id_transacao, tipo, valor, descricao, categoria, data):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE transacoes SET tipo=?, valor=?, descricao=?, categoria=?, data=? WHERE id=?
        """, (tipo.lower(), valor, descricao, categoria, data, id_transacao))
        conn.commit()
    finally:
        conn.close()

def limpar_banco_dados():
    """Limpa todas as transações e reinicia o contador de IDs."""
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transacoes")
        # Opcional: limpa as metas também se desejar um 'reset' total
        # cursor.execute("DELETE FROM metas")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='transacoes'")
        conn.commit()
    finally:
        conn.close()
