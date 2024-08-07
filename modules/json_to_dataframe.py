import os
import json
import pandas as pd

JSON_DIR = "jsons"
CSV_DIR = "dados"

def json_to_csv(json_path):
    """
    Convert JSON data from a file into CSV format.

    Args:
    - json_path: The full path of the JSON file to process.
    """
    with open(json_path, "r") as file:
        json_data = file.read()
    json_filename = os.path.basename(json_path)
    execute_all_functions(json_data, json_filename)

def execute_all_functions(json_data, json_filename):
    """
    Processes JSON data, converts it to DataFrames, and exports to CSV files.

    Args:
    - json_data: A JSON string containing the data to be processed.
    - json_filename: The name of the JSON file for naming CSV files.
    """
    # Step 1: Convert JSON to Dictionary
    response_dict = json.loads(json_data)
    
    # Example JSON objects
    json_objects = response_dict["Instrumento_Compra_Venda"]
    
    # Step 2: Extract Unidade and Empreendimento
    unidade = json_objects["Unidade"]
    empreendimento = json_objects["Empreendimento"]
    
    # Step 3: Process JSON into DataFrames
    dataframes, keys = process_json_to_dataframes(json_objects, unidade, empreendimento)
    
    # Step 4: Export DataFrames to CSV
    export_dataframes_to_csv(dataframes, keys, json_filename)

def process_json_to_dataframes(json_objects, unidade, empreendimento):
    """
    Processes JSON objects to extract data into pandas DataFrames.

    Args:
    - json_objects: Dictionary of JSON objects containing the data to be processed.
    - unidade: Value of Unidade to be added to each DataFrame.
    - empreendimento: Value of Empreendimento to be added to each DataFrame.

    Returns:
    - dataframes: List of DataFrames created from the JSON objects.
    - keys: List of keys for naming the DataFrames.
    """
    dataframes = []
    keys = []

    for key, value in json_objects.items():
        if isinstance(value, dict) and key not in ['Unidade', 'Empreendimento']:
            df = pd.DataFrame([value])
            
            # Only insert columns if they do not already exist
            if "Unidade" not in df.columns:
                df.insert(0, "Unidade", unidade)
            if "Empreendimento" not in df.columns:
                df.insert(1, "Empreendimento", empreendimento)
                
            # Append DataFrame and key
            dataframes.append(df)
            keys.append(f"{key}")

    return dataframes, keys

def export_dataframes_to_csv(dataframes, keys, json_filename):
    """
    Exports a list of dataframes to CSV files in a specified folder.

    Args:
    - dataframes: List of pandas DataFrame objects to export.
    - keys: List of keys corresponding to each DataFrame for naming the CSV files.
    - json_filename: The name of the JSON file for naming CSV files.
    """
    if not os.path.exists(CSV_DIR):
        os.makedirs(CSV_DIR)
    
    # Itera sobre os dataframes e suas chaves
    for df, key in zip(dataframes, keys):
        # Define o caminho do arquivo
        file_path = os.path.join(CSV_DIR, f"{key}.csv")
        
        # Verifica se o arquivo CSV já existe
        if os.path.exists(file_path):
            # Lê o CSV existente
            existing_df = pd.read_csv(file_path)
            
            # Verifica se a unidade já existe
            if df['Unidade'].iloc[0] in existing_df['Unidade'].values:
                print(f"Contrato {df['Unidade'].iloc[0]} já existe no CSV {key}.csv")
                continue  # Pula a adição desta linha
            else:
                # Adiciona os dados ao CSV existente sem adicionar o header
                df.to_csv(file_path, index=False, mode='a', header=False)
        else:
            # Cria o arquivo CSV com o header
            df.to_csv(file_path, index=False, mode='w', header=True)
