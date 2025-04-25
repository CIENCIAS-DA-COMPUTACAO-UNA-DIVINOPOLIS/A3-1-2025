import streamlit as st
import sqlite3
import pandas as pd

# Conexão com o banco de dados
def conectar_bd():
    return sqlite3.connect("biblioteca.db")

# Consulta com filtros
def consultar_acertos(nome_usuario, codigo_livro, status):
    conn = conectar_bd()
    cursor = conn.cursor()

    query = "SELECT nome_usuario, codigo_livro, titulo_livro, data_emprestimo, data_devolucao, status, multa FROM emprestimos WHERE 1=1"
    params = []

    if nome_usuario:
        query += " AND nome_usuario LIKE ?"
        params.append(f"%{nome_usuario}%")
    
    if codigo_livro:
        query += " AND codigo_livro LIKE ?"
        params.append(f"%{codigo_livro}%")
    
    if status != "Todos":
        query += " AND status = ?"
        params.append(status)

    cursor.execute(query, params)
    resultados = cursor.fetchall()
    conn.close()
    
    return resultados

# --- INTERFACE ---
st.title("📚 Consulta de Acertos da Biblioteca")

st.markdown("Filtre os acertos por usuário, código do livro ou status:")

# Filtros
nome_usuario = st.text_input("🔍 Nome do usuário")
codigo_livro = st.text_input("📕 Código do livro")
status = st.selectbox("📌 Status do empréstimo", ["Todos", "Em aberto", "Devolvido", "Multa"])

# Botão para consultar
if st.button("Consultar"):
    dados = consultar_acertos(nome_usuario, codigo_livro, status)

    if dados:
        df = pd.DataFrame(dados, columns=["Usuário", "Código do Livro", "Título", "Data Empréstimo", "Data Devolução", "Status", "Multa"])
        st.success(f"{len(df)} resultado(s) encontrado(s).")
        st.dataframe(df)
    else:
        st.warning("Nenhum resultado encontrado com os filtros fornecidos.")
