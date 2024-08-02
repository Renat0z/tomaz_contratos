import os
import json
import re
import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from openai import OpenAI
# client = OpenAI()

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração dos diretórios
JSON_DIR = "jsons"
CONTRACTS_DIR = "contratos"

# Configuração da chave da API OpenAI a partir das variáveis de ambiente
openai_api_key = os.getenv('OPENAI_API_KEY')

# Criar a instância do modelo
llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=openai_api_key  # Adicione a chave da API aqui
)

def create_directories():       
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def json_chat(prompt):
    st.info("Extraindo as informações com o chatgpt (aguarde...)")
    system_message = "Você é um assistente útil projetado para gerar JSON."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        )
    return response.choices[0].message.content

def extract_data_from_pdf(file_path):
    """
    Extrai dados relevantes do contrato em PDF e salva como JSON usando a API do ChatGPT.
    
    Args:
    - file_path (str): Caminho para o arquivo PDF.
    """
    text = extract_text_from_pdf(file_path)
    json_content = json_chat(text)
    
    if json_content:
        try:
            json_data = json.loads(json_content)
        except json.JSONDecodeError as e:
            st.error(f"Erro ao decodificar JSON: {e}")
            return
        
        json_path = os.path.join(JSON_DIR, os.path.basename(file_path).replace(".pdf", ".json"))
        with open(json_path, "w") as json_file:
            json.dump(json_data, json_file)
        st.success(f"Dados do PDF {os.path.basename(file_path)} extraídos e salvos como JSON.")
    else:
        st.error(f"Falha ao extrair dados do PDF {os.path.basename(file_path)}.")

