import streamlit as st

class FilterHandler:
    def __init__(self, df):
        self.df = df

    def apply_filters(self):
        # Mover os filtros para a sidebar
        tipos = st.sidebar.multiselect(
            "Filtrar por Tipo", 
            self.df["Tipo"].unique(), 
            default=self.df["Tipo"].unique()
        )
        categorias = st.sidebar.multiselect(
            "Filtrar por Categoria", 
            self.df["Categoria"].unique(), 
            default=self.df["Categoria"].unique()
        )
        
        df_filtrado = self.df[self.df["Tipo"].isin(tipos) & self.df["Categoria"].isin(categorias)]
        
        # Mostrar informações sobre os filtros aplicados
        if len(df_filtrado) != len(self.df):
            st.sidebar.success(f"📊 {len(df_filtrado)} de {len(self.df)} registros selecionados")
        
        return df_filtrado
