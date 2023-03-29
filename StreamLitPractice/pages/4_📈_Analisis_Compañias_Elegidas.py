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


def show_fundamentales(company_opt):
    my_dict = {
        'Colgate-Palmolive': """Colgate-Palmolive Company is a consumer products company that markets 
        its products throughout the world. 
        The Company's products include toothpaste, toothbrushes, shampoos, deodorants, bar and liquid soaps, dishwashing liquid, and laundry products, as well as pet nutrition products for cats and dogs."""
        , "Costco":"""Costco Wholesale Corporation is a membership warehouse club The Company sells all kinds of food, automotive supplies, toys, hardware, sporting goods, jewelry, electronics, apparel, health, and beauty aids, as well as other goods. Costco Wholesale serves customers worldwide."""
        , "General Mills":"""General Mills, Inc. operates as a food company. The Company manufactures and markets branded consumer foods. General Mills serves customers worldwide."""
        , "Hershey's":"""The Hershey Company manufactures chocolate and sugar confectionery products. The Company's principal products includes chocolate and sugar confectionery products, gum and mint refreshment products, and pantry items, such as baking ingredients, toppings, and beverages."""
        , "Kimberly-Clark":"""Kimberly-Clark Corporation is a global health and hygiene company that manufactures and provides consumer products. The Company's products include diapers, tissues, paper towels, incontinence care products, surgical gowns, and disposable face masks. Kimberly-Clark's products are sold in countries around the world."""
        , "Coca-Cola company": """The Coca-Cola Company manufactures, markets, and distributes soft drink concentrates and syrups. The Company also distributes and markets juice and juice-drink products. Coca-Cola distributes its products to retailers and wholesalers worldwide."""
        , "Mondelez International": """Mondelez International, Inc. is a food and beverage company. The Company manufactures and markets packaged food products, including snacks, beverages, cheese, convenient meals, and other packaged grocery products. Mondelez International sells its products worldwide."""
        , "Monster Beverage":"""Monster Beverage Corporation operates as a holding company. The Company, through its subsidiaries, markets and distributes energy drinks. Monster Beverage serves customers worldwide."""
        , "PepsiCo": """PepsiCo, Inc. operates foods and beverages businesses. The Company manufactures markets and sells a variety of grain-based snacks, carbonated and non-carbonated beverages, and foods. PepsiCo serves customers worldwide."""
        , "Walmart": """Walmart Inc. operates discount stores, supercenters, and neighborhood markets. The Company offers merchandise such as apparel, house wares, small appliances, electronics, musical instruments, books, home improvement, shoes, jewelry, toddler, games, household essentials, pets, pharmaceutical products, party supplies, and automotive tools. Walmart serves customers worldwide"""
    
        
    }

    st.markdown(f"### {company_opt}")
    st.markdown(my_dict[company_opt])


company_opt = company_opt(get_selected)

col1, col2 = st.columns([2,1])

with col1:
    tab1, tab2, tab3, tab4 = st.tabs([f"Evolución Spy vs {company_opt}", f"Evolución {company_opt}", "Evolución SPY", "Info"])
    with tab1:
        plot_spy_selected(company_opt, get_selected, 0, spy_5, df_5, get_metrics)
    with tab2:
        plot_spy_selected(company_opt, get_selected, 1, spy_5, df_5, get_metrics)
    with tab3:
        plot_spy_selected(company_opt, get_selected, 2, spy_5, df_5, get_metrics)
    with tab4:
        show_fundamentales(company_opt)
with col2:
    plot_metrics(spy_5, df_5, company_opt, get_selected, get_metrics)

get_inflacion()