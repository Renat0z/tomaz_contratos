import streamlit as st
from modules.upload_pdf import create_directories as create_upload_directories, upload_pdf_contracts
from modules.extrator_pdf import create_directories as create_extractor_directories
from modules.list_buyers import show_buyers

def main():
    st.title("Gerenciamento de Contratos PDF")
    create_upload_directories()
    create_extractor_directories()
    
    st.header("Upload de Contratos (PDF/ZIP)")
    upload_pdf_contracts()
    
    st.header("Informações de Contratos")
    show_buyers()

if __name__ == "__main__":
    main()
