import streamlit as st
from models.dashboard import DashboardFinanceiro

st.set_page_config(page_title="Dashboard Financeiro", layout="wide", page_icon=":bar_chart:")

def main():
    dashboard = DashboardFinanceiro()
    dashboard.run()

if __name__ == "__main__":
    main()
