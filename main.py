import streamlit as st
from modules.contratos import main as contratos_main
from modules.upload_excel import main as excel_main
from modules.listar_planilhas import main as listar_planilhas_main

def main():
    st.sidebar.title("Menu")
    option = st.sidebar.selectbox("Selecione a funcionalidade", ["Gerenciamento de Contratos PDF", "Upload de Planilhas Excel", "Listar Planilhas Excel"])

    if option == "Gerenciamento de Contratos PDF":
        contratos_main()
    elif option == "Upload de Planilhas Excel":
        excel_main()
    elif option == "Listar Planilhas Excel":
        listar_planilhas_main()

if __name__ == "__main__":
    main()
