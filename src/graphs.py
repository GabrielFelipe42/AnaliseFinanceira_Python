import streamlit as st
import plotly.express as px
import pandas as pd

class GraphGenerator:
    def __init__(self, df):
        self.df = df.copy()

    def pie_chart(self):
        st.subheader("📊 Distribuição por Categoria")
        df_despesas = self.df[self.df["Tipo"] == "Despesa"]
        if not df_despesas.empty:
            df_group = df_despesas.groupby("Categoria")["Valor"].sum().reset_index()
            fig = px.pie(df_group, names="Categoria", values="Valor", title="Despesas por Categoria")
            st.plotly_chart(fig, use_container_width=True)

    def line_chart(self):
        st.subheader("📈 Evolução do Saldo")
        self.df["Saldo"] = self.df["Valor"].where(self.df["Tipo"] == "Receita", -self.df["Valor"])
        df_saldo = self.df.groupby("Data")["Saldo"].sum().cumsum().reset_index()
        fig = px.line(df_saldo, x="Data", y="Saldo", title="Saldo Acumulado")
        st.plotly_chart(fig, use_container_width=True)
