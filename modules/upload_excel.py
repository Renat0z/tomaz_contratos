import streamlit as st
import os
import pandas as pd

# Configuração do diretório base
BASE_SPREADSHEETS_DIR = "planilhas"

def create_directories():
    if not os.path.exists(BASE_SPREADSHEETS_DIR):
        os.makedirs(BASE_SPREADSHEETS_DIR)

def save_uploaded_file(uploaded_file, save_path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

def upload_excel_sheets(uploaded_files, selected_year):
    year_dir = os.path.join(BASE_SPREADSHEETS_DIR, selected_year)
    if not os.path.exists(year_dir):
        os.makedirs(year_dir)

    for uploaded_file in uploaded_files:
        save_path = os.path.join(year_dir, uploaded_file.name)
        save_uploaded_file(uploaded_file, save_path)
        st.success(f"Arquivo {uploaded_file.name} salvo com sucesso no diretório {selected_year}.")

def extract_data_from_excel(file_path):
    """
    Extrai dados financeiros das planilhas Excel.
    
    Args:
    - file_path (str): Caminho para o arquivo Excel.
    
    Returns:
    - pd.DataFrame: Dados extraídos da planilha.
    """
    df = pd.read_excel(file_path)
    return df

def main():
    st.title("Upload de Planilhas Excel")
    create_directories()
    
    st.header("Upload de Planilhas (Excel)")
    uploaded_excel_files = st.file_uploader("Selecione arquivos Excel", type=["xlsx"], accept_multiple_files=True)
    
    # Seleção de ano
    year_option = st.selectbox("Selecione o ano para salvar as planilhas", ["2024", "2025", "Outro"])
    
    if year_option == "Outro":
        new_year = st.text_input("Digite o novo ano")
        if new_year.isdigit() and st.button("Criar"):
            if not os.path.exists(os.path.join(BASE_SPREADSHEETS_DIR, new_year)):
                os.makedirs(os.path.join(BASE_SPREADSHEETS_DIR, new_year))
                st.success(f"Pasta para o ano {new_year} criada com sucesso.")
            else:
                st.warning(f"Pasta para o ano {new_year} já existe.")
        selected_year = new_year
    else:
        selected_year = year_option

    if st.button("Submeter Arquivos Excel"):
        if uploaded_excel_files:
            upload_excel_sheets(uploaded_excel_files, selected_year)
        else:
            st.warning("Nenhum arquivo Excel selecionado para upload.")

if __name__ == "__main__":
    main()
