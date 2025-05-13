# v3 Falta integrar banco de dados grupo fernando e ao site principal


from nicegui import ui
import sqlite3
import pandas as pd
import os

# --- Criação do banco e dados de teste ---
def criar_banco_e_inserir_dados():
    if not os.path.exists("biblioteca.db"):
        conn = sqlite3.connect("biblioteca.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT NOT NULL,
            codigo_livro TEXT NOT NULL,
            titulo_livro TEXT NOT NULL,
            data_emprestimo TEXT NOT NULL,
            data_devolucao TEXT,
            status TEXT NOT NULL,
            multa REAL DEFAULT 0
        )
        """)

        dados = [
            ("Ana Paula", "L001", "O senhor dos Anéis - A sociedade do Anel", "2024-04-01", "2024-04-15", "Devolvido", 0.0),
            ("Carlos Silva", "L002", "Harry Potter e a Pedra Filosofal", "2024-04-10", None, "Em aberto", 0.0),
            ("João Souza", "L003", "Hábitos Atômicos", "2024-03-15", "2024-04-20", "Multa", 12.5),
            ("Marina Rocha", "L004", "Dom Quixote", "2024-04-05", "2024-04-22", "Devolvido", 0.0),
        ]

        cursor.executemany("""
        INSERT INTO emprestimos (nome_usuario, codigo_livro, titulo_livro, data_emprestimo, data_devolucao, status, multa)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, dados)

        conn.commit()
        conn.close()

# --- Consulta ---
def consultar_acertos(nome_usuario, codigo_ou_titulo, status):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()

    query = """
    SELECT nome_usuario, codigo_livro, titulo_livro, data_emprestimo, data_devolucao, status, multa 
    FROM emprestimos 
    WHERE 1=1
    """
    params = []

    if nome_usuario:
        query += " AND nome_usuario LIKE ?"
        params.append(f"%{nome_usuario}%")
    
    if codigo_ou_titulo:
        query += " AND (codigo_livro LIKE ? OR titulo_livro LIKE ?)"
        params.append(f"%{codigo_ou_titulo}%")
        params.append(f"%{codigo_ou_titulo}%")
    
    if status != "Todos":
        query += " AND status = ?"
        params.append(status)

    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()
    
    return resultados

# --- Consulta da interface ---
def consultar():
    dados = consultar_acertos(nome_input.value, codigo_input.value, status_input.value)
    if dados:
        df = pd.DataFrame(dados, columns=["Usuário", "Código", "Título", "Empréstimo", "Devolução", "Status", "Multa"])
        tabela_resultado.rows = df.to_dict(orient="records")
        mensagem.text = f"{len(df)} resultado(s) encontrado(s)."
        mensagem.style("color: green")
    else:
        tabela_resultado.rows = []
        mensagem.text = "Nenhum resultado encontrado com os filtros fornecidos."
        mensagem.style("color: orange")

# --- Dark Mode Switch ---
dark = ui.dark_mode()
with ui.row().classes("justify-end w-full pr-4 pt-2"):
    ui.button('🌙', on_click=dark.enable)
    ui.button('☀️', on_click=dark.disable)

# --- Topo: Título ---
with ui.column().classes("w-full items-center pt-4"):
    ui.label("📚 Sistema da Biblioteca").classes("text-3xl font-bold")
    ui.label("Filtre os acertos por usuário, código ou título do livro e status").classes("text-lg")

# --- Meio: Inputs e Botão ---
with ui.row().classes("w-full justify-center items-center py-12"):
    nome_input = ui.input("🔍 Nome do usuário").classes("w-64")
    codigo_input = ui.input("📘 Código ou Título do Livro").classes("w-64")
    status_input = ui.select(["Todos", "Em aberto", "Devolvido", "Multa"], value="Todos", label="📌 Status do empréstimo").classes("w-64")
    ui.button("🔎 Consultar Empréstimos", on_click=consultar).classes("mt-4")

# --- Parte de baixo: Tabela e resultado ---
with ui.column().classes("items-center w-full pt-6"):
    tabela_resultado = ui.table(columns=[
        {'name': 'Usuário', 'label': 'Usuário', 'field': 'Usuário', 'sortable': True},
        {'name': 'Código', 'label': 'Código do Livro', 'field': 'Código', 'sortable': True},
        {'name': 'Título', 'label': 'Título', 'field': 'Título', 'sortable': True},
        {'name': 'Empréstimo', 'label': 'Data Empréstimo', 'field': 'Empréstimo', 'sortable': True},
        {'name': 'Devolução', 'label': 'Data Devolução', 'field': 'Devolução', 'sortable': True},
        {'name': 'Status', 'label': 'Status', 'field': 'Status', 'sortable': True},
        {'name': 'Multa', 'label': 'Multa', 'field': 'Multa', 'sortable': True},
    ], rows=[], row_key='Código').classes('w-full max-w-6xl')

    mensagem = ui.label().classes("text-md py-4")

# --- Execução ---
criar_banco_e_inserir_dados()
ui.run()
