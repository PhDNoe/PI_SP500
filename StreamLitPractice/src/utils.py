import streamlit as st
import pandas as pd
import datetime as dt




def str2date(str, format="%Y-%m-%d"):
    """
    Convierte un string a datetime.date
    """
    return dt.datetime.strptime(str, format).date()



def date2str(date, format="%Y-%m-%d"):
    """
    Convierte un datetime.date a string
    """
    return date.strftime(format)



def get_ticker_opt(sp500):
    """
    Obtiene la lista de compañias que forman parte del sp500
    """
    lista_opc = sp500['Symbol'].tolist()
    lista_opc.insert(0, "Only SPY")
    return lista_opc



def get_sp500_sectors(sp500):
    """
    Obtiene la lista de sectores que forman parte del sp500    
    """
    sectors = sp500['GICS Sector'].unique().tolist()
    return sectors


def get_spy_difference(spy, spy_short, crisis_opt, crisis_dict):
    """
    Obtiene la diferencia de valores del SPY en un rango de fechas
    """
    
    date_dict = crisis_dict()
    if crisis_opt!= "Ninguna en particular":        
        spy_filter = spy[spy["Date"].between(date_dict[crisis_opt][0],date_dict[crisis_opt][1])]        
        spy_min_date_price = spy_filter.loc[spy_filter['Close'].idxmin(),["Date", "Close"]]
        spy_max_date_price = spy_filter.loc[spy_filter['Close'].idxmax(),["Date", "Close"]]

        spy_min_price = spy_min_date_price["Close"]
        spy_max_price = spy_max_date_price["Close"]

        spy_min_date = spy_min_date_price["Date"]
        spy_max_date = spy_max_date_price["Date"]
    else:        
        spy_filter = spy_short.copy()
        spy_min_date = spy_filter["Date"].min()
        spy_max_date = spy_filter["Date"].max()
        spy_min_price = spy_filter.loc[spy_filter["Date"] == spy_min_date,"Close"].values[0]
        spy_max_price = spy_filter.loc[spy_filter["Date"] == spy_max_date,"Close"].values[0]
        print(spy_max_price)
    

    if spy_max_date > spy_min_date:
        spy_ini = spy_min_price
        spy_fin = spy_max_price
        spy_ini_date = spy_min_date
        spy_fin_date = spy_max_date
    else:
        spy_ini = spy_max_price
        spy_fin = spy_min_price
        spy_ini_date = spy_max_date
        spy_fin_date = spy_min_date

    delta_spy = round(100*(spy_fin - spy_ini)/(spy_ini),2)


    print("----------------------------------------------------------")
    print("Ini spy --> ", spy_ini)
    print("Fin spy --> ", spy_fin)
    print("Ini spy date --> ", spy_ini_date)
    print("Fin spy date --> ", spy_fin_date)
    print("Delta spy % --> ", delta_spy)
    print("-----------------------------------------------------------")

    return spy_ini, spy_fin, delta_spy, spy_ini_date, spy_fin_date



    

def get_company_difference(df, df_short, ticker, crisis_opt, crisis_dict):
    """
    Obtiene la diferencia de valores de una compañia en un rango dado de fechas
    """
    
    date_dict = crisis_dict()
    print("Ticker --> ", ticker)
    
    if crisis_opt != "Ninguna en particular":        
        df_filter = df[['Date', ticker]]
        df_filter = df_filter.loc[~df_filter[ticker].isna()]

    else:
        df_filter = df_short[['Date', ticker]]
        df_filter = df_filter.loc[~df_filter[ticker].isna()]
        
        
    
    print("Min date --> ", df_filter["Date"].min().date())
    print("Max date --> ", df_filter["Date"].max().date())
    print("crisis date ini --> ", str2date(date_dict[crisis_opt][0]))
    print("crisis date fin --> ", str2date(date_dict[crisis_opt][1]))

    

    if crisis_opt!="Ninguna en particular":
        if df_filter["Date"].min().date() <= str2date(date_dict[crisis_opt][0]) and df_filter["Date"].max().date() >= str2date(date_dict[crisis_opt][1]):
            df_filter = df[df["Date"].between(date_dict[crisis_opt][0],date_dict[crisis_opt][1])]
        else:
            print("Compañia fuera del rango de fechas estudiado")
            return None, None, None, None, None
    
    df_min_date_price = df_filter.loc[df_filter[ticker].idxmin(),["Date", ticker]]
    df_max_date_price = df_filter.loc[df_filter[ticker].idxmax(),["Date", ticker]]

    df_min_price = df_min_date_price[ticker]
    df_max_price = df_max_date_price[ticker]

    df_min_date = df_min_date_price["Date"]
    df_max_date = df_max_date_price["Date"]

    if df_max_date >df_min_date:
        df_ini = df_min_price
        df_fin = df_max_price
        df_ini_date = df_min_date
        df_fin_date = df_max_date
    else:
        df_ini = df_max_price
        df_fin = df_min_price
        df_ini_date = df_max_date
        df_fin_date = df_min_date

    delta_df = round(100*(df_fin - df_ini)/(df_ini),2)
    print("Ini df --> ", df_ini)
    print("Fin df --> ", df_fin)
    print("Delta df % --> ", delta_df)

    return df_ini, df_fin, delta_df, df_ini_date, df_fin_date



def crisis_dict():
    """
    Retorna un diccionario con las fechas de las crisis econmicas
    """
    
    today = dt.datetime.now()
    today = today.strftime('%Y-%m-%d')
    date_dict = {
        # "Ninguna en particular": ['2000-01-01',today],
        "Ninguna en particular": ['2000-01-01','2023-03-01'],
        "Burbuja dot com":  ['2000-01-01','2004-01-01'],
        "Burbuja Subprime": ['2006-01-01','2010-01-01'],
        "Pandemia Covid": ['2020-02-01','2020-04-01']
    }

    return date_dict




def crisis_options():

    crisis_op = ["Ninguna en particular","Burbuja dot com","Burbuja Subprime", "Pandemia Covid"]

    return crisis_op

