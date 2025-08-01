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
            
            # Calcular porcentagens para o hover
            df_group["Porcentagem"] = (df_group["Valor"] / df_group["Valor"].sum() * 100).round(2)
            df_group["Valor_Formatado"] = df_group["Valor"].apply(lambda x: f"R$ {x:,.2f}")
            # CORREÇÃO: Adicionar o símbolo % na formatação
            df_group["Porcentagem_Formatada"] = df_group["Porcentagem"].apply(lambda x: f"{x}%")
            
            fig = px.pie(
                df_group, 
                names="Categoria", 
                values="Valor", 
                title="Despesas por Categoria"
            )
            
            # Customizar o hover template
            fig.update_traces(
                hovertemplate="<b>%{label}</b><br>" +
                             "Valor: %{customdata[0]}<br>" +
                             "<extra></extra>",
                customdata=df_group[["Valor_Formatado", "Porcentagem_Formatada"]].values,
                textinfo='label+percent',
                textposition='inside'
            )
            
            # Melhorar a aparência do gráfico
            fig.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.01
                ),
                font=dict(size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Nenhuma despesa encontrada para gerar o gráfico de pizza.")

    def line_chart(self):
        st.subheader("📈 Evolução do Saldo")
        if not self.df.empty:
            # Criar uma cópia para não modificar o DataFrame original
            df_saldo = self.df.copy()
            
            # Calcular saldo considerando receitas como positivo e despesas como negativo
            df_saldo["Saldo"] = df_saldo["Valor"].where(df_saldo["Tipo"] == "Receita", -df_saldo["Valor"])
            
            # Agrupar por data e calcular saldo acumulado
            df_saldo_diario = df_saldo.groupby("Data")["Saldo"].sum().reset_index()
            df_saldo_diario["Saldo_Acumulado"] = df_saldo_diario["Saldo"].cumsum()
            
            # Formatação para hover
            df_saldo_diario["Data_Formatada"] = df_saldo_diario["Data"].dt.strftime("%d/%m/%Y")
            df_saldo_diario["Saldo_Diario_Formatado"] = df_saldo_diario["Saldo"].apply(
                lambda x: f"R$ {x:,.2f}" if x >= 0 else f"-R$ {abs(x):,.2f}"
            )
            df_saldo_diario["Saldo_Acumulado_Formatado"] = df_saldo_diario["Saldo_Acumulado"].apply(
                lambda x: f"R$ {x:,.2f}" if x >= 0 else f"-R$ {abs(x):,.2f}"
            )
            
            fig = px.line(
                df_saldo_diario, 
                x="Data", 
                y="Saldo_Acumulado", 
                title="Evolução do Saldo Acumulado",
                markers=True
            )
            
            # Customizar o hover template
            fig.update_traces(
                hovertemplate="<b>Data:</b> %{customdata[0]}<br>" +
                             "<b>Saldo do Dia:</b> %{customdata[1]}<br>" +
                             "<b>Saldo Acumulado:</b> %{customdata[2]}<br>" +
                             "<extra></extra>",
                customdata=df_saldo_diario[["Data_Formatada", "Saldo_Diario_Formatado", "Saldo_Acumulado_Formatado"]].values,
                line=dict(width=3),
                marker=dict(size=8)
            )
            
            # Colorir a linha baseada no saldo (verde para positivo, vermelho para negativo)
            fig.update_traces(
                line_color='green' if df_saldo_diario["Saldo_Acumulado"].iloc[-1] >= 0 else 'red'
            )
            
            # Adicionar linha de referência no zero
            fig.add_hline(
                y=0, 
                line_dash="dash", 
                line_color="gray", 
                annotation_text="Linha de Equilíbrio",
                annotation_position="bottom right"
            )
            
            # Melhorar layout - CORRIGIDO
            fig.update_layout(
                xaxis_title="Data",
                yaxis_title="Saldo Acumulado (R$)",
                font=dict(size=12),
                hovermode='x unified',
                # Formatação do eixo Y movida para cá
                yaxis=dict(
                    tickformat=",.2f", 
                    tickprefix="R$ "
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Mostrar métricas complementares
            col1, col2, col3 = st.columns(3)
            with col1:
                saldo_atual = df_saldo_diario["Saldo_Acumulado"].iloc[-1]
                st.metric(
                    "💰 Saldo Atual", 
                    f"R$ {saldo_atual:,.2f}",
                    delta=f"R$ {df_saldo_diario['Saldo'].iloc[-1]:,.2f}" if len(df_saldo_diario) > 1 else None
                )
            with col2:
                total_receitas = self.df[self.df["Tipo"] == "Receita"]["Valor"].sum()
                st.metric("📈 Total Receitas", f"R$ {total_receitas:,.2f}")
            with col3:
                total_despesas = self.df[self.df["Tipo"] == "Despesa"]["Valor"].sum()
                st.metric("📉 Total Despesas", f"R$ {total_despesas:,.2f}")
        else:
            st.warning("⚠️ Nenhum dado encontrado para gerar o gráfico de evolução.")
