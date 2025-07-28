import streamlit as st
import os
from data_loader import DataLoader
from filters import FilterHandler
from graphs import GraphGenerator

class DashboardFinanceiro:
    def __init__(self):
        self.df = None
        self.filtered_df = None

    def run(self):
        loader = DataLoader()
        df = loader.load()
        
        with open(os.path.join("models", "../financas_exemplo.csv"), "rb") as f:
            st.download_button(
                label="📥 Baixar CSV de exemplo",
                data=f,
                file_name="financas_exemplo.csv",
                mime="text/csv"
            )

        if df is not None:
            self.df = df

            st.subheader("📋 Dados Carregados")
            st.dataframe(self.df)

            # Aplicar filtros
            filters = FilterHandler(self.df)
            self.filtered_df = filters.apply_filters()

            # Gerar gráficos
            graphs = GraphGenerator(self.filtered_df)
            graphs.pie_chart()
            graphs.line_chart()
        else:
            st.info("📎 Por favor, envie um arquivo CSV para visualizar o dashboard.")
