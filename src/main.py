import streamlit as st
from models.dashboard import DashboardFinanceiro

st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

def main():
    st.title("💰 Dashboard Financeiro")
    dashboard = DashboardFinanceiro()
    dashboard.run()

if __name__ == "__main__":
    main()
