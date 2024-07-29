import streamlit as st
import os
import zipfile
from modules.extrator_pdf import extract_data_from_pdf

# Configuração dos diretórios
CONTRACTS_DIR = "contratos"

def create_directories():
    if not os.path.exists(CONTRACTS_DIR):
        os.makedirs(CONTRACTS_DIR)

def save_uploaded_file(uploaded_file, save_path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

def upload_pdf_contracts():
    uploaded_files = st.file_uploader("Selecione arquivos PDF ou ZIP", type=["pdf", "zip"], accept_multiple_files=True)
    if st.button("Submeter Arquivos PDF/ZIP"):
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if uploaded_file.type == "application/pdf":
                    save_path = os.path.join(CONTRACTS_DIR, uploaded_file.name)
                    save_uploaded_file(uploaded_file, save_path)
                    st.success(f"Arquivo {uploaded_file.name} salvo com sucesso.")
                    extract_data_from_pdf(save_path)
                elif uploaded_file.type == "application/x-zip-compressed" or uploaded_file.name.endswith(".zip"):
                    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                        zip_ref.extractall(CONTRACTS_DIR)
                    st.success(f"Arquivos do ZIP {uploaded_file.name} extraídos com sucesso.")
                    for filename in os.listdir(CONTRACTS_DIR):
                        if filename.endswith(".pdf"):
                            extract_data_from_pdf(os.path.join(CONTRACTS_DIR, filename))
        else:
            st.warning("Nenhum arquivo PDF ou ZIP selecionado para upload.")
