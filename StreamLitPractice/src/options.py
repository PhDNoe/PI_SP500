import streamlit as st
from src.utils import get_ticker_opt, get_sp500_sectors
import datetime as dt



def ticker_opt(sp500):
    """"
    Retorna un menu desplegable con todas las compañias del sp500
    """

    msg = "Filtrar por compañia"
    opt_list = get_ticker_opt(sp500)


    option = st.sidebar.selectbox(
    msg,
    opt_list)

    return option


def sector_opt(sp500):
    """
    Retorna un menu desplegable con todos los sectores del sp500
    """
    msg = "Filtrar por sector"
    sectors = get_sp500_sectors(sp500)
    option = st.sidebar.selectbox(
        msg,
        sectors
    )
    return option



def wanna_plot_spy():
    """
    Retorna un checkbox para indicar si se desea o no plotear el SPY
    """
    msg = "Plotear SP500 index?"
    cb= st.sidebar.checkbox(msg, value=True)
    return cb



def wanna_plot_company():
    """
    Retorna un checkbox para indicar si se desea o no plotear la evolucion de la compañia
    """
    msg = "Plotear Compañia?"
    cb= st.sidebar.checkbox(msg, value=False)    
    return cb



def wanna_plot_zoom():
    """
    Retorna un checkbox para indicar si se desea o no plotear un zoom de los precios en torno a una determinada crisis economica
    """
    msg = "Plotear zoom Crisis"
    cb = st.sidebar.checkbox(msg, value=False)
    return cb



def date_slider():
    """
    Retorna un slider doble para poder modificar el rango  de fechas que se desea analizar
    
    """
    max_date = dt.date.today()
    min_date = dt.date(2000,1,1)
    msg = 'Seleccionar rango de fechas'

    format = 'YYYY-MM-DD'


    slide = st.slider(msg,
        min_value=min_date, max_value=max_date, value = (min_date, max_date), format=format) 


    return slide




def crisis_option():
    """
    Retorna un menu desplegable que indica las posibles crisis economicas que se pueden analizar
    """
    msg = 'Crisis economicas'

    crisis_list = ["Ninguna en particular","Burbuja dot com","Burbuja Subprime", "Pandemia Covid"]
    opt = st.sidebar.selectbox(
        msg,
        crisis_list)

    return opt


def show_selected_options(min_str_date, max_str_date, tk_opt, crisis_opt):
    """
    Muestra por pantalla las opciones seleccionadas, junto con el rango de fechas utilizado para el filtrado
    
    """
    # st.markdown("---")
    st.markdown("#### Filtros aplicados")
    st.markdown(f'* **Rango de fechas:** :blue[{ min_str_date}] - :blue[{max_str_date}]')
    st.markdown(f'* **Empresa seleccinada:** :blue[{tk_opt}]')    
    st.markdown(f'* **Crisis economica:** :red[{crisis_opt}]')
    # st.markdown("---")