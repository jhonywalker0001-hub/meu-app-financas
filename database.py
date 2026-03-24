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
    try:
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
    finally:
        conn.close()

def limpar_banco_dados():
    """Função que resolve o erro de importação citada nos logs."""
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transacoes")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='transacoes'")
        conn.commit()
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
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]
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

def deletar_transacao(id_transacao):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transacoes WHERE id = ?", (id_transacao,))
        conn.commit()
    finally:
        conn.close()
