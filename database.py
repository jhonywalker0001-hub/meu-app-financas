import sqlite3
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import os
from kivy.utils import platform

def conectar():
    nome_db = "financas.db"
    if platform == 'android':
        try:
            from android.storage import app_storage_path
            caminho = os.path.join(app_storage_path(), nome_db)
        except ImportError:
            caminho = nome_db
    else:
        caminho = nome_db
    conn = sqlite3.connect(caminho, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        valor REAL NOT NULL,
        descricao TEXT,
        categoria TEXT DEFAULT 'Geral',
        data TEXT NOT NULL,
        ativo INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_data ON transacoes(data)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tipo ON transacoes(tipo)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_categoria ON transacoes(categoria)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ativo ON transacoes(ativo)")
    
    conn.commit()
    conn.close()

def criar_tabela_metas():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria TEXT UNIQUE,
        valor_limite REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    
    CATEGORIAS_PADRAO = [
        "Alimentação", "Transporte", "Moradia", "Saúde", 
        "Lazer", "Educação", "Salário", "Freelance", "Outros"
    ]
    
    for cat in CATEGORIAS_PADRAO:
        cursor.execute(
            "INSERT OR IGNORE INTO metas (categoria, valor_limite) VALUES (?, 0)", 
            (cat,)
        )
    
    conn.commit()
    conn.close()

def normalizar_data(data_str=None):
    if not data_str:
        return datetime.now().strftime("%d/%m/%Y")
    
    data_str = str(data_str).strip()
    
    if '-' in data_str and len(data_str) == 10:
        try:
            dt = datetime.strptime(data_str, "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except ValueError:
            pass
    
    return data_str

def validar_tipo(tipo):
    tipo = str(tipo).lower().strip()
    return tipo if tipo in ('receita', 'despesa') else 'despesa'

def calcular_saldo():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN tipo='receita' THEN valor ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN tipo='despesa' THEN valor ELSE 0 END), 0)
        FROM transacoes
        WHERE ativo = 1
    """)
    res = cursor.fetchone()
    conn.close()
    return res[0] - res[1]

def adicionar_transacao(tipo, valor, descricao, categoria="Geral", data=None):
    tipo = validar_tipo(tipo)
    valor = abs(float(valor))
    descricao = str(descricao).strip()[:100]
    categoria = str(categoria).strip()[:50] or "Geral"
    data = normalizar_data(data)
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transacoes (tipo, valor, descricao, categoria, data)
        VALUES (?, ?, ?, ?, ?)
    """, (tipo, valor, descricao, categoria, data))
    conn.commit()
    conn.close()

def listar_transacoes(ativo=True):
    conn = conectar()
    cursor = conn.cursor()
    
    if ativo:
        cursor.execute("SELECT * FROM transacoes WHERE ativo = 1 ORDER BY id DESC")
    else:
        cursor.execute("SELECT * FROM transacoes ORDER BY id DESC")
    
    colunas = [c[0] for c in cursor.description]
    dados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    conn.close()
    return dados

def resumo_transacoes(mes_ano=None):
    if not mes_ano:
        mes_ano = datetime.now().strftime("%m/%Y")
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN tipo='receita' THEN valor ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN tipo='despesa' THEN valor ELSE 0 END), 0)
        FROM transacoes
        WHERE data LIKE ? AND ativo = 1
    """, (f'%{mes_ano}',))
    res = cursor.fetchone()
    conn.close()
    return res[0], res[1]

def resumo_por_categoria(mes_ano=None):
    if not mes_ano:
        mes_ano = datetime.now().strftime("%m/%Y")
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT categoria, 
               COALESCE(SUM(valor), 0) as total,
               COUNT(*) as quantidade
        FROM transacoes 
        WHERE tipo='despesa' AND data LIKE ? AND ativo = 1
        GROUP BY categoria
        ORDER BY total DESC
    """, (f'%{mes_ano}',))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def definir_meta(categoria, valor):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO metas (categoria, valor_limite) VALUES (?, ?)
        ON CONFLICT(categoria) DO UPDATE SET valor_limite=excluded.valor_limite
    """, (categoria, float(valor)))
    conn.commit()
    conn.close()

def obter_metas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT categoria, valor_limite FROM metas")
    dados = cursor.fetchall()
    conn.close()
    return {cat: val for cat, val in dados}

def obter_caminho_exportacao(nome_arquivo):
    if platform == 'android':
        try:
            from android.storage import primary_external_storage_path
            downloads_path = os.path.join(primary_external_storage_path(), 'Download')
            os.makedirs(downloads_path, exist_ok=True)
            return os.path.join(downloads_path, nome_arquivo)
        except ImportError:
            pass
    return nome_arquivo

def exportar_para_excel(nome_arquivo, mes_filtro=None):
    caminho = obter_caminho_exportacao(nome_arquivo)
    conn = conectar()
    
    query = "SELECT data, categoria, descricao, tipo, valor FROM transacoes WHERE ativo = 1"
    params = ()
    
    if mes_filtro:
        query += " AND data LIKE ?"
        params = (f'%{mes_filtro}',)
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    
    df.to_excel(caminho, index=False, engine='openpyxl')
    return caminho

def exportar_para_pdf(nome_arquivo, mes_filtro=None):
    caminho = obter_caminho_exportacao(nome_arquivo)
    conn = conectar()
    cursor = conn.cursor()
    
    query = "SELECT data, categoria, descricao, tipo, valor FROM transacoes WHERE ativo = 1"
    params = ()
    
    if mes_filtro:
        query += " AND data LIKE ?"
        params = (f'%{mes_filtro}',)
    
    cursor.execute(query, params)
    dados = cursor.fetchall()
    conn.close()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(190, 10, "Relatorio Financeiro", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(30, 8, "Data", 1)
    pdf.cell(35, 8, "Categoria", 1)
    pdf.cell(70, 8, "Descricao", 1)
    pdf.cell(25, 8, "Tipo", 1)
    pdf.cell(30, 8, "Valor", 1, ln=True)
    
    pdf.set_font("Helvetica", "", 10)
    total_receitas = 0
    total_despesas = 0
    
    for row in dados:
        data, categoria, descricao, tipo, valor = row
        pdf.cell(30, 8, str(data), 1)
        pdf.cell(35, 8, str(categoria)[:15], 1)
        pdf.cell(70, 8, str(descricao)[:35], 1)
        pdf.cell(25, 8, str(tipo), 1)
        pdf.cell(30, 8, f"R$ {valor:.2f}", 1, ln=True)
        
        if tipo == 'receita':
            total_receitas += valor
        else:
            total_despesas += valor
    
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, f"Total Receitas: R$ {total_receitas:.2f}", ln=True)
    pdf.cell(0, 10, f"Total Despesas: R$ {total_despesas:.2f}", ln=True)
    pdf.cell(0, 10, f"Saldo: R$ {total_receitas - total_despesas:.2f}", ln=True)
    
    pdf.output(caminho)
    return caminho

def deletar_transacao(id_transacao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE transacoes SET ativo = 0 WHERE id = ?", (id_transacao,))
    conn.commit()
    conn.close()

def restaurar_transacao(id_transacao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE transacoes SET ativo = 1 WHERE id = ?", (id_transacao,))
    conn.commit()
    conn.close()

def atualizar_transacao(id_transacao, tipo, valor, descricao, categoria, data):
    tipo = validar_tipo(tipo)
    valor = abs(float(valor))
    descricao = str(descricao).strip()[:100]
    categoria = str(categoria).strip()[:50]
    data = normalizar_data(data)
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transacoes 
        SET tipo=?, valor=?, descricao=?, categoria=?, data=?
        WHERE id=?
    """, (tipo, valor, descricao, categoria, data, id_transacao))
    conn.commit()
    conn.close()

def limpar_banco_dados(confirmar=False):
    if not confirmar:
        raise ValueError("Confirme com confirmar=True para apagar tudo!")
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacoes")
    cursor.execute("DELETE FROM metas")
    conn.commit()
    conn.close()
