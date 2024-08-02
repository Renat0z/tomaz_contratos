import os
import json
import pandas as pd

def execute_all_functions(json_data):
    """
    Executes all functions to process JSON data, convert it to DataFrames, and export to CSV files.
    
    Args:
    - json_data: A JSON string containing the data to be processed.
    """
    # Step 1: Convert JSON to Dictionary
    response_dict = json.loads(json_data)
    
    # Step 2: Extract Unidade and Empreendimento
    unidade = response_dict["Unidade"]
    empreendimento = response_dict["Empreendimento"]
    
    # Step 3: Process JSON into DataFrames
    dataframes, keys = process_json_to_dataframes(response_dict, unidade, empreendimento)
    
    # Step 4: Export DataFrames to CSV
    export_dataframes_to_csv(dataframes, keys)

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
            if "Unidade" not in df.columns:
                df.insert(0, "Unidade", unidade)
            if "Empreendimento" not in df.columns:
                df.insert(1, "Empreendimento", empreendimento)
            dataframes.append(df)
            keys.append(f"{key}")

    return dataframes, keys

def export_dataframes_to_csv(dataframes, keys):
    """
    Exports a list of dataframes to CSV files in a specified folder.
    
    Args:
    - dataframes: List of pandas DataFrame objects to export.
    - keys: List of keys corresponding to each DataFrame for naming the CSV files.
    """
    folder_name = "dados"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    for df, key in zip(dataframes, keys):
        file_path = os.path.join(folder_name, f"{key}.csv")
        if not os.path.exists(file_path):
            df.to_csv(file_path, index=False, mode='w', header=True)
        else:
            df.to_csv(file_path, index=False, mode='a', header=False)

