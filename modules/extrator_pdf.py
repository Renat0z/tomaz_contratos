import os
import json
import re
import fitz  # PyMuPDF
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

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

def chat_with_openai(prompt):
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    return response.content

def extract_json(response):
    json_match = re.search(r'\{.*?\}', response, re.DOTALL)
    if json_match:
        return json_match.group(0)
    else:
        return None

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def process_text_with_openai(text):
    user_input = f"""seja um auditor meticuloso de contas de uma construtora e avalie o contrato delimitado pelas tags <contrato></contrato>.
<contrato>
{text}
</contrato>
    
Extraia todas as informações possiveis do texto em <contrato> em formato json.
Se houver informações relevantes que não estão nesse exemplo, pode adicionar ao json.

Cada chave pode ter apenas um valor, pois serão submetidos a uma planilha.

aqui está um exemplo:

==========================
     QUADRO RESUMO
==========================
Empreendimento: {{quadro_resumo.Empreendimento}}
Unidade: {{quadro_resumo.Unidade}}

==========================
        VENDEDORA
==========================
Nome Vendedora: {{vendedora["Nome Vendedora"]}}
CNPJ: {{vendedora.CNPJ}}
Endereço: {{vendedora.Endereço}}
CEP: {{vendedora.CEP}}

==========================
        COMPRADOR
==========================
Nome: {{comprador.Nome}}
Data de Nascimento: {{comprador["Data de Nascimento"]}}
Nacionalidade: {{comprador.Nacionalidade}}
Profissão: {{comprador.Profissão}}
RG: {{comprador.RG}}
CPF: {{comprador.CPF}}
Estado Civil: {{comprador["Estado Civil"]}}
Data de Casamento: {{comprador["Data de Casamento"]}}
Regime: {{comprador.Regime}}
Telefone: {{comprador.Telefone}}
Email: {{comprador.Email}}
Endereço: {{comprador.Endereço}}
Bairro: {{comprador.Bairro}}
Cidade: {{comprador.Cidade}}
Estado: {{comprador.Estado}}
CEP: {{comprador.CEP}}

==========================
        TERRENO
==========================
Descrição: {{terreno.Descrição}}
Localização: {{terreno.Localização}}
Matrícula: {{terreno.Matrícula}}
Inscrição Imobiliária: {{terreno["Inscrição Imobiliária"]}}

==========================
      LOTEAMENTO
==========================
Nome: {{loteamento.Nome}}
Registro: {{loteamento.Registro}}
Aprovação Prefeitura: {{loteamento["Aprovação Prefeitura"]}}
Processo: {{loteamento.Processo}}
GRAPROHAB: {{loteamento.GRAPROHAB}}
Prazo Conclusão: {{loteamento["Prazo Conclusão"]}}

==========================
          LOTE
==========================
Quadra: {{lote.Quadra}}
Lote: {{lote.Lote}}
Frente: {{lote.Frente}}
Lado Direito: {{lote["Lado Direito"]}}
Lado Esquerdo: {{lote["Lado Esquerdo"]}}
Fundos: {{lote.Fundos}}
Área: {{lote.Área}}
Matrícula: {{lote.Matrícula}}

==========================
      PAGAMENTO
==========================
Preço do Imóvel: {{pagamento["Preço do Imóvel"]}}
Parcela Sinal: {{pagamento["Parcela Sinal"]}}
Parcelas Mensais 1:
    Quantidade: {{pagamento["Parcelas Mensais 1"].Quantidade}}
    Valor: {{pagamento["Parcelas Mensais 1"].Valor}}
    Primeira Parcela: {{pagamento["Parcelas Mensais 1"]["Primeira Parcela"]}}
Parcelas Mensais 2:
    Quantidade: {{pagamento["Parcelas Mensais 2"].Quantidade}}
    Valor: {{pagamento["Parcelas Mensais 2"].Valor}}
    Primeira Parcela: {{pagamento["Parcelas Mensais 2"]["Primeira Parcela"]}}
Reajuste: {{pagamento.Reajuste}}
Juros: {{pagamento.Juros}}

==========================
MORA E RESCISÃO
==========================
Juros Mora: {{mora_rescisao["Juros Mora"]}}
Multa: {{mora_rescisao.Multa}}
Rescisão: {{mora_rescisao.Rescisão}}

==========================
RESPONSABILIDADES DO COMPRADOR
==========================
Impostos: {{responsabilidades_comprador.Impostos}}
Transferência de Titularidade: {{responsabilidades_comprador["Transferência Titularidade"]}}

==========================
CESSÃO E TRANSFERÊNCIA
==========================
Anuência Vendedora: {{cessao_transferencia["Anuência Vendedora"]}}
Custo: {{cessao_transferencia.Custo}}

==========================
DIREITO DE ARREPENDIMENTO
==========================
Prazo: {{direito_arrependimento.Prazo}}
Devolução: {{direito_arrependimento.Devolução}}

==========================
DEMAIS CONDIÇÕES
==========================
Cláusulas Ratificadas: {{demais_condicoes["Cláusulas Ratificadas"]}}

==========================
     ASSINATURAS
==========================
Comprador: {{assinaturas.Comprador}}
Testemunhas:
    Nome: {{assinaturas.Testemunhas[0].Nome}}
    CPF: {{assinaturas.Testemunhas[0].CPF}}
    Nome: {{assinaturas.Testemunhas[1].Nome}}
    CPF: {{assinaturas.Testemunhas[1].CPF}}
Data: {{assinaturas.Data}}

    """
    response = chat_with_openai(user_input)
    return extract_json(response)

def extract_data_from_pdf(file_path):
    """
    Extrai dados relevantes do contrato em PDF e salva como JSON usando a API do ChatGPT.
    
    Args:
    - file_path (str): Caminho para o arquivo PDF.
    """
    text = extract_text_from_pdf(file_path)
    json_content = process_text_with_openai(text)
    
    if json_content:
        json_path = os.path.join(JSON_DIR, os.path.basename(file_path).replace(".pdf", ".json"))
        with open(json_path, "w") as json_file:
            json.dump(json.loads(json_content), json_file)
        st.success(f"Dados do PDF {os.path.basename(file_path)} extraídos e salvos como JSON.")
    else:
        st.error(f"Falha ao extrair dados do PDF {os.path.basename(file_path)}.")

