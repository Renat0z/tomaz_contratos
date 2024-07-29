import streamlit as st
import os
import pandas as pd

# Configuração do diretório base
BASE_SPREADSHEETS_DIR = "planilhas"

def get_years():
    """
    Retorna uma lista dos anos disponíveis no diretório de planilhas.
    """
    return [name for name in os.listdir(BASE_SPREADSHEETS_DIR) if os.path.isdir(os.path.join(BASE_SPREADSHEETS_DIR, name))]

def list_sheets(year):
    """
    Retorna uma lista de arquivos Excel para o ano selecionado.
    """
    year_dir = os.path.join(BASE_SPREADSHEETS_DIR, year)
    return [f for f in os.listdir(year_dir) if f.endswith(".xlsx")]

def show_sheet(file_path):
    """
    Exibe o conteúdo da planilha no worksheet "(D) Recebiveis".
    """
    df = pd.read_excel(file_path, sheet_name="(D) Recebiveis")

    if "filter_col" not in st.session_state:
        st.session_state.filter_col = df.columns[0]
    if "search_term" not in st.session_state:
        st.session_state.search_term = ""

    filter_col = st.selectbox("Selecione a coluna para filtrar", df.columns, key="filter_col")
    search_term = st.text_input("Pesquisar na planilha", key="search_term")

    if st.session_state["search_term"]:
        df = df[df[st.session_state["filter_col"]].astype(str).str.contains(st.session_state["search_term"], case=False, na=False)]

    st.dataframe(df)
    if st.button("Voltar"):
        del st.session_state["file_path"]
        del st.session_state["filter_col"]
        del st.session_state["search_term"]
        show_sheets()

def show_sheets():
    """
    Exibe a lista de arquivos Excel com opção de visualização.
    """
    years = get_years()
    selected_year = st.selectbox("Selecione o ano", years, key="selected_year")
    search_term = st.text_input("Pesquisar planilhas", key="sheet_search_term")

    if selected_year:
        sheets = list_sheets(selected_year)
        filtered_sheets = [sheet for sheet in sheets if search_term.lower() in sheet.lower()]

        st.write("## Planilhas")
        cols = st.columns([3, 1])  # Define a largura das colunas
        headers = ["Nome da Planilha", "Ações"]
        for col, header in zip(cols, headers):
            col.write(f"**{header}**")

        for sheet in filtered_sheets:
            cols = st.columns([3, 1])  # Redefine as colunas para cada linha de dados
            cols[0].write(sheet)
            if cols[1].button(f"Ver planilha {sheet}"):
                st.session_state["file_path"] = os.path.join(BASE_SPREADSHEETS_DIR, selected_year, sheet)
                show_sheet(st.session_state["file_path"])

def main():
    st.title("Listar Planilhas")
    if "file_path" in st.session_state:
        show_sheet(st.session_state["file_path"])
    else:
        show_sheets()

if __name__ == "__main__":
    main()
