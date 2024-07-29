import streamlit as st
import os
import json
import zipfile
import PyPDF2

# Configuração dos diretórios
CONTRACTS_DIR = "contratos"
JSON_DIR = "jsons"

def create_directories():
    if not os.path.exists(CONTRACTS_DIR):
        os.makedirs(CONTRACTS_DIR)
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)

def save_uploaded_file(uploaded_file, save_path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

def extract_data_from_pdf(file_path):
    """
    Extrai dados relevantes do contrato em PDF e salva como JSON.
    
    Args:
    - file_path (str): Caminho para o arquivo PDF.
    """
    data = {}
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        # Exemplo de extração de informações específicas (ajustar conforme necessário)
        if "Empreendimento:" in text:
            data["empreendimento"] = text.split("Empreendimento:")[1].split("\n")[0].strip()
        if "Unidade:" in text:
            data["unidade"] = text.split("Unidade:")[1].split("\n")[0].strip()
        if "Nome comprador 1:" in text:
            data["nome_comprador"] = text.split("Nome comprador 1:")[1].split("\n")[0].strip()
        if "CPF/MF:" in text:
            data["cpf_comprador"] = text.split("CPF/MF:")[1].split("\n")[0].strip()
        if "Preço do Imóvel:" in text:
            data["preco_imovel"] = text.split("Preço do Imóvel:")[1].split("\n")[0].strip()

    json_path = os.path.join(JSON_DIR, os.path.basename(file_path).replace(".pdf", ".json"))
    with open(json_path, "w") as json_file:
        json.dump(data, json_file)
    st.success(f"Dados do PDF {os.path.basename(file_path)} extraídos e salvos como JSON.")

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

def count_buyers():
    """
    Conta o número de contratos (PDF) e exibe na tela.
    """
    num_contracts = len([f for f in os.listdir(CONTRACTS_DIR) if f.endswith(".pdf")])
    st.write(f"Número de contratos: {num_contracts}")

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
    pdf_path = os.path.join(CONTRACTS_DIR, contract)
    json_path = os.path.join(JSON_DIR, contract.replace(".pdf", ".json"))

    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        st.success(f"Arquivo PDF {contract} deletado com sucesso.")
    if os.path.exists(json_path):
        os.remove(json_path)
        st.success(f"Arquivo JSON {contract.replace('.pdf', '.json')} deletado com sucesso.")

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
                delete_files(selected_contract)
                show_buyers()
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

def main():
    st.title("Gerenciamento de Contratos PDF")
    create_directories()
    
    st.header("Upload de Contratos (PDF/ZIP)")
    upload_pdf_contracts()
    
    st.header("Informações de Contratos")
    count_buyers()
    show_buyers()

if __name__ == "__main__":
    main()
