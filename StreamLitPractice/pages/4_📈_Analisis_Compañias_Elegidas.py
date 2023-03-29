import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import yfinance as yf
from src.page4_5_src.p45_functions import get_selected, plot_spy_selected, company_opt, get_metrics, plot_metrics, get_inflacion


# page layout
st.set_page_config(layout="wide")


st.markdown("### Compañías preseleccionadas - Sector: Consumer Staples")
st.markdown("Consumer Staples: Productos básicos de consumo")




df_5 = pd.read_csv('./data/selected.csv', index_col=0)
df_5.reset_index(inplace=True)
df_5["Date"] =  pd.to_datetime(df_5["Date"], format="%Y-%m-%d")   

spy_5 = pd.read_csv('./data/spy_5.csv')
spy_5["Date"] =  pd.to_datetime(spy_5["Date"], format="%Y-%m-%d")   




company_opt = company_opt(get_selected)

col1, col2 = st.columns([2,1])

with col1:
    tab1, tab2, tab3 = st.tabs([f"Evolución Spy vs {company_opt}", f"Evolución {company_opt}", "Evolución SPY"])
    with tab1:
        plot_spy_selected(company_opt, get_selected, 0, spy_5, df_5, get_metrics)
    with tab2:
        plot_spy_selected(company_opt, get_selected, 1, spy_5, df_5, get_metrics)
    with tab3:
        plot_spy_selected(company_opt, get_selected, 2, spy_5, df_5, get_metrics)

with col2:
    plot_metrics(spy_5, df_5, company_opt, get_selected, get_metrics)

get_inflacion()