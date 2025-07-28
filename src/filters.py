import streamlit as st

class FilterHandler:
    def __init__(self, df):
        self.df = df

    def apply_filters(self):
        tipos = st.multiselect("Filtrar por Tipo", self.df["Tipo"].unique(), default=self.df["Tipo"].unique())
        categorias = st.multiselect("Filtrar por Categoria", self.df["Categoria"].unique(), default=self.df["Categoria"].unique())
        df_filtrado = self.df[self.df["Tipo"].isin(tipos) & self.df["Categoria"].isin(categorias)]
        return df_filtrado
