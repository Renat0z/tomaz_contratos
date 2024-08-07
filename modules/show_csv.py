import streamlit as st
import os
import pandas as pd

CSV_DIR = "dados"

def show_csv_files():
    """
    Displays available CSV files in the 'dados' directory and allows users to view them in Streamlit.
    """
    st.title("Dados em CSV")
    
    if not os.path.exists(CSV_DIR) or len(os.listdir(CSV_DIR)) == 0:
        st.info("Nenhum arquivo CSV disponível.")
        return
    
    csv_files = [f for f in os.listdir(CSV_DIR) if f.endswith('.csv')]
    if not csv_files:
        st.info("Nenhum arquivo CSV encontrado.")
        return

    selected_csv = st.selectbox("Selecione um arquivo CSV para visualizar", csv_files)
    
    if selected_csv:
        df = pd.read_csv(os.path.join(CSV_DIR, selected_csv))
        st.write(f"## {selected_csv}")
        st.dataframe(df)

        if st.button("Deletar CSV"):
            os.remove(os.path.join(CSV_DIR, selected_csv))
            st.success(f"{selected_csv} deletado com sucesso.")
            st.experimental_rerun()
