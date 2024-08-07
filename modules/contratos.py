import os
import streamlit as st
from modules.upload_pdf import create_directories as create_upload_directories, upload_pdf_contracts
from modules.extrator_pdf import create_directories as create_extractor_directories, extract_data_from_pdf
from modules.list_buyers import show_buyers
from modules.show_csv import show_csv_files

def main():
    st.title("Gerenciamento de Contratos PDF")
    
    # Ensure necessary directories are created
    create_upload_directories()
    create_extractor_directories()
    
    st.header("Upload de Contratos (PDF/ZIP)")
    uploaded_files = upload_pdf_contracts()

    if uploaded_files:
        st.header("Extraindo dados e convertendo para CSV")
        for file_path in uploaded_files:
            extract_data_from_pdf(file_path)
    
    st.header("Informações de Contratos")
    show_buyers()
    
    st.header("Dados CSV")
    show_csv_files()

if __name__ == "__main__":
    main()
