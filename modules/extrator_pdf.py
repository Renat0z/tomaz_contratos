import os
import json
import re
import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from modules.json_to_dataframe import json_to_csv  # Import the function



###
### CHAVES DE API

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

# CRIAR DIRETÓRIOS jsons e contratos

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
    # msg de log para o usuário
    st.info("Extraindo as informações com o chatgpt (aguarde...)")
    
    # Enviar a solicitação para a API do ChatGPT (retona um JSON)    
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
    Escreva um JSON com os dados do contrato abaixo, exatamente como no exemplo em <modelo>. 
    O nome das chaves são os headers de uma planilha, por isso as chaves devem ser exatamente como no modelo.
    
    Eu odeio pessoas que alteram as chaves do JSON. Não faça isso.
    Não acrescente nem diminua o número de chaves do JSON. Não faça isso.
    Não altere o tipo de dado de cada chave. Não faça isso.
    Não altere a ordem das chaves. Não faça isso.
    
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
        
        # Save JSON data to a file
        json_path = os.path.join(JSON_DIR, os.path.basename(file_path).replace(".pdf", ".json"))
        with open(json_path, "w") as json_file:
            json.dump(json_data, json_file)           
        st.success(f"Dados do PDF {os.path.basename(file_path)} extraídos e salvos como JSON.")
        
        # Convert JSON to CSV using the json_path
        json_to_csv(json_path)
    else:
        st.error(f"Falha ao extrair dados do PDF {os.path.basename(file_path)}.")


