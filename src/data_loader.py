import streamlit as st
import pandas as pd

class DataLoader:
    def load(self):
        file = st.file_uploader("Faça upload do seu arquivo CSV", type=["csv"])
        if file:
            try:
                df = pd.read_csv(file, parse_dates=["Data"])
                df["Data"] = pd.to_datetime(df["Data"])
                df = df.sort_values("Data")
                return df
            except Exception as e:
                st.error(f"Erro ao carregar o CSV: {e}")
        return None
