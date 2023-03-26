import streamlit as st
import pandas as pd
import datetime as dt



def get_list_path():
    """
    Retorna una lista con los path de los archivos que debemos cargar
    
    """
    list_path = []
    sp500_list_path = './data/sp500list.csv'
    list_path.append(sp500_list_path)

    sp500_companies_path = './data/tk502.csv'
    list_path.append(sp500_companies_path)

    spy_path = './data/SPY.csv'
    list_path.append(spy_path)
    return list_path

    

@st.cache_data
def load_data(path):
    """
    Carga el archivo pasado por parametro en un dataframe.
    Cachea el resultado
    """
    data = pd.read_csv(path)    
    return data


def parse_date(df, col, my_format='%Y-%m-%d'):
    """
    Funcion para parsear las columnas con fechas. Retorna un dataframe

    > df: dataframe, el dataframe que contiene una o varias columnas con fechas
    > col: Nombre de la columna de fecha


    """
    df[col] =  pd.to_datetime(df[col], format=my_format)    
    return df



def load_all(list_path):
    """
    Carga y retorna todos los dataframes a utilizar.

    > list_path: lista de strings, contiene todos los paths de los archivos a cargar
    """
    sp500_list_path,sp500_companies_path,spy_path = list_path
    sp500 = load_data(sp500_list_path)
    sp500_companies = load_data(sp500_companies_path)
    spy = load_data(spy_path)
    
    # Parse Dates
    
    sp500_companies = parse_date(sp500_companies, "Date")
    spy = parse_date(spy,"Date")
    return sp500, sp500_companies, spy



def df_with_time_filter(sp500_companies, spy, min_str_date="2000-01-01", max_str_date=dt.datetime.now().strftime('%Y-%m-%d')):
    """
    Retorna los dataframes, afectados por el slide de tiempo

    > sp500_companies: dataframe, contiene todos los precios de las compañias
    > spy: dataframe, contiene los precios del SPY
    > min_str_date: string, string que contiene una fecha de inicio (default: 2000-01-01)
    > max_str_date: string, string que contiene la fecha actual
    """
    sp500_comp_short = sp500_companies[sp500_companies['Date'].between(min_str_date,max_str_date)]
    

    spy_short = spy[spy['Date'].between(min_str_date,max_str_date)]
    

    return sp500_comp_short, spy_short