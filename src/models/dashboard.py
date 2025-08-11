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

        # Caminho corrigido para o arquivo de exemplo
        exemplo_path = os.path.join(os.path.dirname(__file__), "..", "financas_exemplo.csv")
        if os.path.exists(exemplo_path):
            with open(exemplo_path, "rb") as f:
                st.download_button(
                    label="📥 Baixar CSV de exemplo",
                    data=f,
                    file_name="financas_exemplo.csv",
                    mime="text/csv"
                )
        else:
            st.warning("Arquivo de exemplo não encontrado. Faça upload do seu próprio CSV.")

        loader = DataLoader()
        df = loader.load()

        if df is not None:
            self.df = df

            # Configurar sidebar quando os dados são carregados
            self._setup_sidebar()

            st.subheader("📋 Dados Carregados")
            st.dataframe(self.df)

            # Aplicar filtros
            filters = FilterHandler(self.df)
            self.filtered_df = filters.apply_filters()

            # Gerar gráficos baseado na seleção do usuário
            self._render_selected_graphs()

    def _setup_sidebar(self):
        """Configura a sidebar com opções de gráficos e filtros"""
        st.sidebar.header("🎛️ Configurações")
        
        # Seção de filtros
        st.sidebar.subheader("🔍 Filtros")
        
        # Seção de gráficos
        st.sidebar.subheader("📊 Gráficos Disponíveis")
        st.sidebar.markdown("Selecione quais gráficos deseja visualizar:")

    def _render_selected_graphs(self):
        """Renderiza os gráficos selecionados pelo usuário"""
        graphs = GraphGenerator(self.filtered_df)
        
        # Opções de gráficos disponíveis
        grafico_pizza = st.sidebar.checkbox("📊 Distribuição por Categoria (Pizza)", value=True)
        grafico_linha = st.sidebar.checkbox("📈 Evolução do Saldo (Linha)", value=True)
        
        # Renderizar gráficos baseado na seleção
        if grafico_pizza:
            graphs.pie_chart()
            
        if grafico_linha:
            graphs.line_chart()
        
        # Mensagem quando nenhum gráfico é selecionado
        if not grafico_pizza and not grafico_linha:
            st.info("👆 Selecione pelo menos um gráfico na sidebar para visualizar os dados.")

