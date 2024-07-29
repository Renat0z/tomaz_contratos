import streamlit as st
import os
import json

# Configuração dos diretórios
JSON_DIR = "jsons"

def list_buyers():
    """
    Extrai o nome do comprador e o contrato de todos os JSONs.
    """
    buyers = []
    for json_file in os.listdir(JSON_DIR):
        if json_file.endswith(".json"):
            with open(os.path.join(JSON_DIR, json_file), "r") as file:
                data = json.load(file)
                buyers.append({
                    "contrato": json_file.replace(".json", ".pdf"),
                    "nome_comprador": data.get("nome_comprador", "Desconhecido")
                })
    return buyers

def json_to_markdown(json_data, level=1):
    markdown = ""
    
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            markdown += f"{'#' * level} {key}\n\n"
            markdown += json_to_markdown(value, level + 1)
    elif isinstance(json_data, list):
        for item in json_data:
            markdown += json_to_markdown(item, level)
    else:
        markdown += f"{json_data}\n\n"
    
    return markdown

def filter_buyers(buyers, term, filter_by):
    """
    Filtra a lista de compradores com base no termo de pesquisa e no tipo de filtro.
    """
    if filter_by == "Nome do Comprador":
        return [buyer for buyer in buyers if term.lower() in buyer["nome_comprador"].lower()]
    elif filter_by == "Contrato":
        return [buyer for buyer in buyers if term.lower() in buyer["contrato"].lower()]
    return buyers

def delete_files(contract):
    """
    Deleta os arquivos PDF e JSON associados a um contrato.
    
    Args:
    - contract (str): Nome do arquivo do contrato PDF (ex: 'contrato1.pdf').
    """
    pdf_path = os.path.join("contratos", contract)
    json_path = os.path.join(JSON_DIR, contract.replace(".pdf", ".json"))

    pdf_deleted = False
    json_deleted = False

    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        pdf_deleted = True
        st.success(f"Arquivo PDF {contract} deletado com sucesso.")
    else:
        st.warning(f"Arquivo PDF {contract} não encontrado.")

    if os.path.exists(json_path):
        os.remove(json_path)
        json_deleted = True
        st.success(f"Arquivo JSON {contract.replace('.pdf', '.json')} deletado com sucesso.")
    else:
        st.warning(f"Arquivo JSON {contract.replace('.pdf', '.json')} não encontrado.")

    return pdf_deleted and json_deleted

def show_buyers(selected_contract=None):
    """
    Exibe na tela os dados dos compradores e um botão que encaminha para uma página onde o JSON é exibido.
    """
    if selected_contract:
        with open(os.path.join(JSON_DIR, selected_contract.replace(".pdf", ".json")), "r") as file:
            json_data = json.load(file)
            markdown_data = json_to_markdown(json_data)
            st.markdown(markdown_data)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Voltar"):
                show_buyers()
        with col2:
            if st.button("Excluir"):
                if delete_files(selected_contract):
                    show_buyers()
                else:
                    st.error("Erro ao deletar os arquivos. Verifique se os arquivos existem.")
    else:
        filter_by = st.selectbox("Filtrar por", ["Nome do Comprador", "Contrato"])
        search_term = st.text_input("Pesquisar")
        buyers = list_buyers()
        filtered_buyers = filter_buyers(buyers, search_term, filter_by)

        st.write("## Compradores")
        cols = st.columns([1, 3, 1])  # Define a largura das colunas
        headers = ["Contrato", "Nome Comprador", "Ações"]
        for col, header in zip(cols, headers):
            col.write(f"**{header}**")

        for buyer in filtered_buyers:
            contrato = buyer["contrato"]
            nome_comprador = buyer["nome_comprador"]
            cols = st.columns([1, 3, 1])  # Redefine as colunas para cada linha de dados
            cols[0].write(contrato)
            cols[1].write(nome_comprador)
            if cols[2].button(f"{contrato}"):
                show_buyers(contrato)
