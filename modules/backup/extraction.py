import PyPDF2
import pandas as pd
import os

markdown += f"{'**' * level}{key}{'**' * level}: \n"

def extract_data_from_pdf(file_path):
    """
    Extrai dados relevantes do contrato em PDF.
    
    Args:
    - file_path (str): Caminho para o arquivo PDF.
    
    Returns:
    - dict: Dados extraídos do PDF.
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

    return data

def extract_data_from_excel(file_path):
    """
    Extrai dados financeiros das planilhas Excel.
    
    Args:
    - file_path (str): Caminho para o arquivo Excel.
    
    Returns:
    - pd.DataFrame: Dados extraídos da planilha.
    """
    df = pd.read_excel(file_path)
    return df

def main():
    # Exemplo de uso das funções de extração
    pdf_example = os.path.join("contratos", "exemplo_contrato.pdf")
    excel_example = os.path.join("planilhas", "2024", "exemplo_planilha.xlsx")

    pdf_data = extract_data_from_pdf(pdf_example)
    excel_data = extract_data_from_excel(excel_example)

    print("Dados extraídos do PDF:")
    print(pdf_data)

    print("Dados extraídos da planilha Excel:")
    print(excel_data.head())

if __name__ == "__main__":
    main()
