import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import yfinance as yf
import ta


def get_selected():
    pre_selected = ["CL", "COST", "GIS", "HSY", "KMB", "KO", "MDLZ", "MNST", "PEP","WMT"]
    pre_selected_names = {"CL":"Colgate-Palmolive", 
                        "COST":"Costco", 
                        "GIS":"General Mills", 
                        "HSY":"Hershey's", 
                        "KMB":"Kimberly-Clark", 
                        "KO":"Coca-Cola company", 
                        "MDLZ":"Mondelez International", 
                        "MNST":"Monster Beverage", 
                        "PEP":"PepsiCo",
                        "WMT": "Walmart"}
    only_names = [x for x in pre_selected_names.values()]
    pre_selected_tickers = {v:k for k,v in pre_selected_names.items()}

    return pre_selected, pre_selected_names, pre_selected_tickers, only_names




df_5 = pd.read_csv('./data/selected.csv', index_col=0)
df_5.reset_index(inplace=True)
df_5["Date"] =  pd.to_datetime(df_5["Date"], format="%Y-%m-%d")   

spy_5 = pd.read_csv('./data/spy_5.csv')
spy_5["Date"] =  pd.to_datetime(spy_5["Date"], format="%Y-%m-%d")   








def company_opt(get_selected):
    """"
    Retorna un menu desplegable con las compañias pre-seleccionadas
    """

    pre_selected, pre_selected_names, pre_selected_tickers, only_names = get_selected()

    msg = "Seleccionar Compañia"
    


    option = st.sidebar.selectbox(
    msg,only_names
    )

    return option




def get_metrics(spy_5, df_5, ticker):
    ini_value_spy = spy_5['Close'].iloc[0]       
    fin_value_spy = spy_5['Close'].iloc[-1]
    delta_p_spy = round(100*(fin_value_spy-ini_value_spy)/ini_value_spy,2)

    
    my_df = df_5.copy()
    my_df = my_df[['Date', ticker]]
    ini_value = my_df.iloc[0,1]
    fin_value = my_df.iloc[-1,1]
    delta_p = round(100*(fin_value-ini_value)/ini_value,2)

    return (ini_value_spy, fin_value_spy, delta_p_spy ), (ini_value, fin_value, delta_p)


def plot_metrics(spy_5, df_5, company_opt, get_selected, get_metrics):
    pre_selected, pre_selected_names, pre_selected_tickers, only_names = get_selected()
    ticker = pre_selected_tickers[company_opt]
    (ini_value_spy, fin_value_spy, delta_p_spy ), (ini_value, fin_value, delta_p) = get_metrics(spy_5, df_5, ticker)

    st.markdown("---")
    st.markdown("#### :blue[**Precio SPY**]")
    st.markdown(":blue[Variación % en 5 años]")
    st.metric("SPY", str(round(fin_value_spy,2))+" u$s", str(delta_p_spy)+ " %")
    st.markdown("---")
    st.markdown(f"#### :blue[**Precio {company_opt} ({ticker})**]")
    st.markdown(":blue[Variación % en 5 años]")
    st.metric(company_opt, str(round(fin_value,2))+" u$s", str(delta_p) +" %")
    st.markdown("---")



def plot_spy_selected(company_opt, get_selected, opt, spy_5, df_5, get_metrics):

    pre_selected, pre_selected_names, pre_selected_tickers, only_names = get_selected()
    ticker = pre_selected_tickers[company_opt]
    (ini_value_spy, fin_value_spy, delta_p_spy ), (ini_value, fin_value, delta_p) = get_metrics(spy_5, df_5, ticker)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)


    if opt==0: # Plotea spy vs compañia
        
        fig, ax = plt.subplots()
        tk = pre_selected_tickers[company_opt]
        sns.lineplot(x="Date", y=tk, data=df_5,ax=ax, label=company_opt)
        sns.lineplot(x="Date", y="Adj Close", data=spy_5, ax=ax, label="Sp500")
        ax.set( xlabel="Fecha", ylabel="Precio")
        ax.tick_params(axis='x', labelrotation=45)                
        plt.suptitle("Comprativa de los ultimos 5 años")
        plt.tight_layout()
        st.pyplot(fig)
    elif opt==1:  # PLotea solo compañia
        fig, ax = plt.subplots()
        tk = pre_selected_tickers[company_opt]
        sns.lineplot(x="Date", y=tk, data=df_5,ax=ax, label=company_opt)        
        ax.text(0.8, 0.1, 'Variación total:\n'+str(delta_p)+" %", horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, bbox=props)
        ax.set(xlabel="Fecha", ylabel="Precio")
        ax.tick_params(axis='x', labelrotation=45)                
        plt.suptitle(f"Evolución de {company_opt} ultimos 5 años")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        fig, ax = plt.subplots()
        sns.lineplot(x="Date", y="Adj Close", data=spy_5, ax=ax, label="Sp500")
        ax.text(0.8, 0.1, 'Variación total:\n'+str(delta_p_spy)+" %", horizontalalignment='center',verticalalignment='center', transform=ax.transAxes, bbox=props)
        ax.set( xlabel="Fecha", ylabel="Precio")
        ax.tick_params(axis='x', labelrotation=45)                
        ax.set(title="Comprativa de los ultimos 5 años SPY")
        plt.tight_layout()
        st.pyplot(fig)

def load_inflation(path):
    inflation = pd.read_csv(path)
    inflation['Year'] = pd.to_datetime(inflation['Year'], format="%Y")   
    inflation['Year'] =inflation['Year'].dt.year.map(lambda x: str(x))
    inflation = inflation[['Year', 'Ave', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
    return inflation


def get_inflacion():
        inflation = load_inflation('./data/Inflation_usa.csv')
        promedio = round(inflation['Ave'].iloc[1:5].mean(),2)
        acumulada = round(inflation['Ave'].iloc[1:5].sum(),2)
        variacion = (inflation['Ave'].iloc[1]-inflation['Ave'].iloc[2])

        cola, colb, colc = st.columns([2,2,2])
        with cola:
            st.metric("Inflación Acumulada", str(acumulada)+" %", variacion)
        with colb:
            st.metric("Inflación Promedio", str(promedio)+" %")



def plot_ma(df_5, nombre):
    # Media movil de 50 dias
    pre_selected, pre_selected_names, pre_selected_tickers, only_names = get_selected()
    ticker = pre_selected_tickers[nombre]
    df_5['SMA50'] = ta.trend.sma_indicator(df_5[ticker], window=50)

    # Media móvil de 100 días
    df_5['SMA100'] = ta.trend.sma_indicator(df_5[ticker], window=100)

    # Graficar los precios de cierre y la media móvil de 50 días
    fig, ax = plt.subplots()
    ax.plot(df_5[ticker], label='Precio de cierre')
    ax.plot(df_5['SMA50'], label='Media móvil de 50 días', color='red')
    ax.plot(df_5['SMA100'], label='Media móvil de 100 días', color='green')
    ax.legend()
    plt.title("Medias moviles de 50 y 100 dias para "+nombre)
    st.pyplot(fig)

def plot_rsi(df_5, nombre):

    pre_selected, pre_selected_names, pre_selected_tickers, only_names = get_selected()
    ticker = pre_selected_tickers[nombre]
    df_5_cpy = df_5.copy()
    df_5_cpy["RSI"] = ta.momentum.rsi(df_5[ticker], window=14)



    # Calcular el RSI con un período de 14 días
    delta = df_5_cpy[ticker].diff()
    gain = delta.mask(delta<0,0)
    loss = -delta.mask(delta>0,0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))

    # Graficar los precios y el RSI
    fig, ax = plt.subplots(2, 1, figsize=(10,8), sharex=True)
    ax[0].plot(df_5_cpy.index, df_5[ticker])
    ax[0].set_ylabel('Precio')
    ax[1].plot(rsi.index, rsi)
    ax[1].set_ylabel('RSI')
    ax[1].axhline(y=30, color='g', linestyle='-')
    ax[1].axhline(y=70, color='r', linestyle='-')
    plt.title("Indice de fuerza relativa para "+nombre)
    st.pyplot(fig)

def plot_ma_rsi(df_5, nombre):  


    # Media movil de 50 dias
    pre_selected, pre_selected_names, pre_selected_tickers, only_names = get_selected()
    ticker = pre_selected_tickers[nombre]
    df_5['SMA50'] = ta.trend.sma_indicator(df_5[ticker], window=50)

    # Media móvil de 100 días
    df_5['SMA100'] = ta.trend.sma_indicator(df_5[ticker], window=100)

    # Graficar los precios de cierre y la media móvil de 50 días
    # Graficar los precios y el RSI
    fig, ax = plt.subplots(2, 1, figsize=(10,8), sharex=True)
    ax[0].plot(df_5[ticker], label='Precio de cierre')
    ax[0].plot(df_5['SMA50'], label='Media móvil de 50 días', color='red')
    ax[0].plot(df_5['SMA100'], label='Media móvil de 100 días', color='green')

    pre_selected, pre_selected_names, pre_selected_tickers, only_names = get_selected()
    ticker = pre_selected_tickers[nombre]
    df_5_cpy = df_5.copy()
    df_5_cpy["RSI"] = ta.momentum.rsi(df_5[ticker], window=14)



    # Calcular el RSI con un período de 14 días
    delta = df_5_cpy[ticker].diff()
    gain = delta.mask(delta<0,0)
    loss = -delta.mask(delta>0,0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))


    # ax[0].plot(df_5_cpy.index, df_5[ticker])
    # ax[0].set_ylabel('Precio')
    ax[1].plot(rsi.index, rsi)
    ax[1].set_ylabel('RSI')
    ax[1].axhline(y=30, color='g', linestyle='-')
    ax[1].axhline(y=70, color='r', linestyle='-')
    plt.title("Indice de fuerza relativa para "+nombre)
    st.pyplot(fig)