import os
import json
import PyPDF2
import streamlit as st

# Configuração dos diretórios
JSON_DIR = "jsons"

def create_directories():
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)

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
