import streamlit as st
import os
from data_loader import DataLoader
from filters import FilterHandler
from graphs import GraphGenerator

#Data,Categoria,Tipo,Valor,Descrição

class DashboardFinanceiro:
    def __init__(self):
        self.df = None
        self.filtered_df = None

    def run(self):
        st.title(":bar_chart: Análise de dados financeiros - Python")
        st.info(
            "📥 **Carregue um arquivo CSV** para começar. Certifique-se de que o arquivo contém as seguintes colunas:\n\n"
            "- **Data**\n"
            "- **Categoria**\n"
            "- **Tipo de Despesa**\n"
            "- **Valor**\n"
            "- **Descrição**\n\n"
            "⬇️ Em caso de dúvidas, você pode baixar um arquivo CSV de exemplo abaixo."
        )
        
        with open(os.path.join("models", "../financas_exemplo.csv"), "rb") as f:
            st.download_button(
                label="📥 Baixar CSV de exemplo",
                data=f,
                file_name="financas_exemplo.csv",
                mime="text/csv"
            )
        
        loader = DataLoader()
        df = loader.load()

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

