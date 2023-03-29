import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

from src.header import header
from src.sp500_plot import plot_sp500
from src.loaders import load_all, parse_date, get_list_path, df_with_time_filter
from src.options import ticker_opt, wanna_plot_spy, date_slider, crisis_option, show_selected_options
from src.options import wanna_plot_company, sector_opt, wanna_plot_zoom
from src.plots import plot_crisis, plot_spy, plot_company_or_spy_or_both, subplot_spy_and_company, plot_zoom_crisis
from src.utils import get_spy_difference, crisis_dict, crisis_options, get_company_difference
from src.KPIs import spy_diff_kpi_movil, company_diff_kpi_movil

# page layout
st.set_page_config(layout="wide")


# All data path
list_path = get_list_path()


# Page Header
header()

# Load all data. Once uploaded, they will remain cached.
sp500, sp500_companies, spy = load_all(list_path)



container1 = st.container()
container2 = st.container()
container3 = st.container()

with container1:
    cont_inner_1 = st.container()
    cola, colb, colc = st.columns([4,1,1])


with container2:
    st.markdown('***')
    col1, col2, col3 = st.columns([3,1,2])


with col1:    
    d_slider = date_slider()

min_str_date = str(d_slider[0])
max_str_date = str(d_slider[1])



# Sidebar
tk_opt = ticker_opt(sp500)  # option, company ticker 
plt_sp500 = wanna_plot_spy() # Checkbox, wanna plot spy index evoution?  True = plot, False = not plot
plt_comp = wanna_plot_company() # Checkbox, wanna plot company evolution? True = plot, False = not plot
# plt_subplot = wanna_subplot_company_and_spy() # Checkbox, wanna subplot?
st.sidebar.markdown("---")
crisis_opt = crisis_option() # Option, financial crises
plt_zoom  = wanna_plot_zoom()
# sector_opt = sector_opt(sp500)


# d_slider = adjust_time_range(crisis_opt)

# Main body
with col3:
    show_selected_options(min_str_date, max_str_date, tk_opt, crisis_opt)

# Filtered dataframes
sp500_comp_short, spy_short = df_with_time_filter(sp500_companies, spy, min_str_date, max_str_date)


st.markdown("---")
# Plot 
with cola:
    
    plot_company_or_spy_or_both(plt_comp, tk_opt, sp500_comp_short, spy_short, plt_sp500, crisis_opt,spy)

    expander = st.expander("Ver Índice y empresa en gráficos separados")
    with expander:
        if tk_opt!="Only SPY":
            subplot_spy_and_company(tk_opt, crisis_opt, spy_short, sp500_comp_short,spy)
        else:
            st.write("No se ha seleccionado ninguna empresa")

    expander2 = st.expander("Ver zoom de crisis Economica seleccionada")   

    with expander2:
        if crisis_opt!="Ninguna en particular":
            if plt_zoom:
                if ((plt_comp and tk_opt!="Only SPY") or plt_sp500):
                    plot_zoom_crisis(tk_opt, crisis_opt, spy, sp500_companies, crisis_dict, crisis_options, plt_zoom, plt_sp500, plt_comp)
                    
                else:
                    st.write("Seleccione las opciones 'Plotear SP500 Index' o seleccione una compañia (y marque la opcion de plotear)")
        else:
            st.write("No se ha seleccionado ninguna crisis en particular")

get_spy_difference(spy, spy_short, crisis_opt, crisis_dict)

if tk_opt!="Only SPY":
    get_company_difference(sp500_companies, sp500_comp_short, tk_opt, crisis_opt, crisis_dict)
    

with cont_inner_1:
    colc_1, colc_2, colc_3 = st.columns([1,1,1])
    with colc_1:
        spy_diff_kpi_movil(spy_short, crisis_dict)
    with colc_3:
        if tk_opt!="Only SPY":
            company_diff_kpi_movil(sp500_comp_short, crisis_dict, tk_opt)
    with colc_2:
        st.write(":violet[Periodo analizado: ]")        
        st.write(f"Fecha inicio: :blue[{min_str_date}]")
        st.write(f"Fecha fin: :blue[{max_str_date}]")
    st.markdown('---')



