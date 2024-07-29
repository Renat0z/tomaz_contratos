import streamlit as st
import os
import zipfile
import pandas as pd

# Configuração dos diretórios
CONTRACTS_DIR = "contratos"
SPREADSHEETS_DIR = os.path.join("planilhas", "2024")

def create_directories():
    if not os.path.exists(CONTRACTS_DIR):
        os.makedirs(CONTRACTS_DIR)
    if not os.path.exists(SPREADSHEETS_DIR):
        os.makedirs(SPREADSHEETS_DIR)

def save_uploaded_file(uploaded_file, save_path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

def upload_pdf_contracts(uploaded_files):
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            save_path = os.path.join(CONTRACTS_DIR, uploaded_file.name)
            save_uploaded_file(uploaded_file, save_path)
            st.success(f"Arquivo {uploaded_file.name} salvo com sucesso.")
        elif uploaded_file.type == "application/x-zip-compressed" or uploaded_file.name.endswith(".zip"):
            with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                zip_ref.extractall(CONTRACTS_DIR)
            st.success(f"Arquivos do ZIP {uploaded_file.name} extraídos com sucesso.")

def upload_excel_sheets(uploaded_files):
    for uploaded_file in uploaded_files:
        save_path = os.path.join(SPREADSHEETS_DIR, uploaded_file.name)
        save_uploaded_file(uploaded_file, save_path)
        st.success(f"Arquivo {uploaded_file.name} salvo com sucesso.")

def main():
    st.title("Upload de Documentos")
    create_directories()

    st.header("Upload de Contratos (PDF/ZIP)")
    uploaded_pdf_files = st.file_uploader("Selecione arquivos PDF ou ZIP", type=["pdf", "zip"], accept_multiple_files=True)

    if st.button("Submeter Arquivos PDF/ZIP"):
        if uploaded_pdf_files:
            upload_pdf_contracts(uploaded_pdf_files)
        else:
            st.warning("Nenhum arquivo PDF ou ZIP selecionado para upload.")
    
    st.header("Upload de Planilhas (Excel)")
    uploaded_excel_files = st.file_uploader("Selecione arquivos Excel", type=["xlsx"], accept_multiple_files=True)

    if st.button("Submeter Arquivos Excel"):
        if uploaded_excel_files:
            upload_excel_sheets(uploaded_excel_files)
        else:
            st.warning("Nenhum arquivo Excel selecionado para upload.")
