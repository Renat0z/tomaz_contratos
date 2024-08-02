import os
import json
import re
import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from openai import OpenAI
client = OpenAI()

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Definir em client a função da OpenAI
client = OpenAI()


###
### DIRETÓRIOS

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


###
### MANIPULAR PDF

# TRANSFORMAR PDF EM TEXTO

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# EXTRAIR DADOS DO TEXTO COM O CHATGPT PARA FORMATO JSON

def json_chat(prompt):
    st.info("Extraindo as informações com o chatgpt (aguarde...)")
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


### PROMPT GPT PARA EXTRAIR DADOS DE UM TEXTO PARA JSON

# carregar template json de dados contrato em contrato_modelo.txt
def load_contract_template():
    with open("templates/contrato_modelo_json.txt", "r") as file:
        return file.read()


# Prompt para extrair dados de um contrato em JSON
def prompt_contrato_to_json(text):
    # Carregar template de contrato em JSON
    template_contrato_json = load_contract_template()
    
    # Prompt para extrair dados de um contrato em JSON
    prompt_contrato_to_json = f"""
    <contrato>
    {text}
    </contrato>

    <modelo>
    {template_contrato_json}
    </modelo>
    """
    return prompt_contrato_to_json



###
### LOOP PARA EXTRAIR DADOS DE VÁRIOS PDFs

def extract_data_from_pdf(file_path):
    """
    Extrai dados relevantes do contrato em PDF e salva como JSON usando a API do ChatGPT.
    
    Args:
    - file_path (str): Caminho para o arquivo PDF.
    """
    # Extrair texto do PDF
    text = extract_text_from_pdf(file_path)
    
    # Extrair dados do texto com o ChatGPT
    prompt_gpt = prompt_contrato_to_json(text)  
    json_contrato = json_chat(prompt_gpt)
    
    if json_contrato:
        try:
            json_data = json.loads(json_contrato)
        except json.JSONDecodeError as e:
            st.error(f"Erro ao decodificar JSON: {e}")
            return
        
        json_path = os.path.join(JSON_DIR, os.path.basename(file_path).replace(".pdf", ".json"))
        with open(json_path, "w") as json_file:
            json.dump(json_data, json_file)
        st.success(f"Dados do PDF {os.path.basename(file_path)} extraídos e salvos como JSON.")
    else:
        st.error(f"Falha ao extrair dados do PDF {os.path.basename(file_path)}.")

