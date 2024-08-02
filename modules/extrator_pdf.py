import os
import json
import re
import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração dos diretórios
JSON_DIR = "jsons"
CONTRACTS_DIR = "contratos"

# Configuração da chave da API OpenAI a partir das variáveis de ambiente
openai_api_key = os.getenv('OPENAI_API_KEY')


if openai_api_key is None:
    raise ValueError("A chave da API OpenAI não foi configurada corretamente. Verifique seu arquivo .env.")

# Criar a instância do modelo
client = OpenAI(api_key=openai_api_key)

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
    st.info("Extraindo as informações com o chatgpt")
    system_message = "Você é um assistente útil projetado para gerar JSON."
    response = client.Completion.create(
        model="gpt-4o-mini",
        prompt=prompt,
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].text.strip()

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

# Chamar a função para criar diretórios ao iniciar o script
create_directories()
