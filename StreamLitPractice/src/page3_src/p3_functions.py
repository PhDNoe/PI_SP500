import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt




def highlight_columns(df, rows=10, color='lightgreen', columns_to_shadow=[], columns_to_show=[], color_n_rows=10):
    highlight = lambda slice_of_df: 'background-color: %s' % color
    sample_df = df.head(rows)
    if len(columns_to_show) != 0:
        sample_df = sample_df[columns_to_show]
    highlighted_df = sample_df.style.applymap(highlight, subset=pd.IndexSlice[:color_n_rows, columns_to_shadow])
    return highlighted_df



def load_inflation(path):
    inflation = pd.read_csv('./data/Inflation_usa.csv')
    inflation['Year'] = pd.to_datetime(inflation['Year'], format="%Y")   
    inflation['Year'] =inflation['Year'].dt.year.map(lambda x: str(x))
    inflation = inflation[['Year', 'Ave', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]
    return inflation



def inflation_container(color_n_rows):
    inflation = load_inflation('./data/Inflation_usa.csv')
    cols = inflation.columns
    cola, colb, colc = st.columns([1,4,1])
    col0, col1, col2 = st.columns([1,4,1])

    with col1:
        st.markdown("#### Datos de la inflación de Estados Unidos")
        st.write(highlight_columns(inflation, rows=24, color='yellow', columns_to_shadow=['Ave'], columns_to_show=cols, color_n_rows=color_n_rows))
        st.caption("Tabla 1: En amarillo se indica la inflación promedio de los últimos 5 años")

    
    if color_n_rows==1:
        h1 = "Promedio de la inflación del último año"
        h2 = """Suma acumulativa de la inflación del último año."""
        promedio = round(inflation['Ave'].iloc[1],2)
        acumulada = round(inflation['Ave'].iloc[1],2)
        variacion = (inflation['Ave'].iloc[1]-inflation['Ave'].iloc[2])
    else:
        h1 = "Promedio de la inflación de los últimos 5 años"
        h2 = f" Suma acumulativa de la inflación de los últimos {color_n_rows} años." 
        promedio = round(inflation['Ave'].iloc[1:color_n_rows].mean(),2)
        acumulada = round(inflation['Ave'].iloc[1:color_n_rows].sum(),2)
        variacion = (inflation['Ave'].iloc[1]-inflation['Ave'].iloc[2])
        
    h3="""La variación se calcula como --> variacion_ultimo_período_completo [%] - Variación_período_anterior [%]
        siendo el período 1 año"""
    st.markdown('---')


    with colb:
        colb1, colb2 = st.columns([1,1])
        with colb1:
            if color_n_rows==1:
                st.metric("Inflación promedio último año", str(promedio)+" %", help=h1)
            else:
                st.metric(f"Inflación promedio últimos {color_n_rows} años", str(promedio)+" %", help=h1)
        with colb2:
            if color_n_rows==1:
                st.metric("Inflación acumulada último año", str(acumulada)+" %", variacion, help=h2)
            else:
                st.metric(f"Inflación acumulada últimos {color_n_rows} años", str(acumulada)+" %", variacion, help=h2)
        st.caption("Nota: "+h3)


def inflation_table(color_n_rows):
    inflation = load_inflation('./data/Inflation_usa.csv')
    cols = inflation.columns
    st.markdown("#### Datos de la inflación de Estados Unidos")
    st.write(highlight_columns(inflation, rows=24, color='yellow', columns_to_shadow=['Ave'], columns_to_show=cols, color_n_rows=color_n_rows))
    st.caption("Tabla 1: En amarillo se indica la inflación promedio de los últimos 5 años")

    
def inflation_metrics(color_n_rows):
    inflation = load_inflation('./data/Inflation_usa.csv')
    cols = inflation.columns
    cola, colb, colc = st.columns([1,4,1])
    


    if color_n_rows==1:
        h1 = "Promedio de la inflación del último año"
        h2 = """Suma acumulativa de la inflación del último año."""
        promedio = round(inflation['Ave'].iloc[1],2)
        acumulada = round(inflation['Ave'].iloc[1],2)
        variacion = (inflation['Ave'].iloc[1]-inflation['Ave'].iloc[2])
    else:
        h1 = "Promedio de la inflación de los últimos 5 años"
        h2 = f" Suma acumulativa de la inflación de los últimos {color_n_rows} años." 
        promedio = round(inflation['Ave'].iloc[1:color_n_rows].mean(),2)
        acumulada = round(inflation['Ave'].iloc[1:color_n_rows].sum(),2)
        variacion = (inflation['Ave'].iloc[1]-inflation['Ave'].iloc[2])
        
    h3="""La variación se calcula como --> variacion_ultimo_período_completo [%] - Variación_período_anterior [%]
        siendo el período 1 año"""
    # st.markdown('---')


    with colb:
        colb1, colb2 = st.columns([1,1])
        with colb1:
            if color_n_rows==1:
                st.metric("Inflación promedio último año", str(promedio)+" %", help=h1)
            else:
                st.metric(f"Inflación promedio últimos {color_n_rows} años", str(promedio)+" %", help=h1)
        with colb2:
            if color_n_rows==1:
                st.metric("Inflación acumulada último año", str(acumulada)+" %", variacion, help=h2)
            else:
                st.metric(f"Inflación acumulada últimos {color_n_rows} años", str(acumulada)+" %", variacion, help=h2)
        # st.caption("Nota: "+h3)




def sector_opt(companies):
    """"
    Retorna un menu desplegable con todos los sectores del sp500
    """

    msg = "Seleccionar sector"
    opt_list = companies['GICS Sector'].unique().tolist()


    option = st.selectbox(
    msg,
    opt_list)

    return option



def plot_sector_vs_spy(sector_dfs, sect_opt, spy_close):
    fig, ax = plt.subplots()
    sns.lineplot(x="Date", y="mean", data=sector_dfs[sect_opt],ax=ax, label="Average of "+sect_opt)
    sns.lineplot(x="Date", y="Close", data=spy_close, ax=ax, label="Sp500")
    ax.set(title="Evolución del SP500 vs sector "+sect_opt, xlabel="Fecha", ylabel="Precio")
    ax.tick_params(axis='x', labelrotation=45)
    st.pyplot(fig)




def plot_sector_vs_spy_delta(spy_close, sector_dfs, sect_opt):

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    (ini_value_spy, fin_value_spy, delta_p_spy ), (ini_value, fin_value, delta_p) = get_metrics(spy_close,sector_dfs, sect_opt)


    my_df = sector_dfs[sect_opt]
    my_df = my_df[['Date', 'mean']]

    fig, ax = plt.subplots(2,1) 
    sns.lineplot(x="Date", y='mean', data=my_df, ax=ax[1], label=sect_opt)
    ax[1].text(0.8, 0.1, 'Variación total:\n'+str(delta_p)+" %", horizontalalignment='center',verticalalignment='center', transform=ax[1].transAxes, bbox=props)
    ax[1].set(title=sect_opt, xlabel="Fecha", ylabel="Precio")
    ax[1].tick_params(axis='x', labelrotation=45)
    plt.suptitle("Variacion")

    sns.lineplot(x="Date", y="Close", data=spy_close, ax=ax[0], label="Sp500")
    ax[0].text(0.8, 0.1, 'Variación total:\n'+str(delta_p_spy)+" %", horizontalalignment='center',verticalalignment='center', transform=ax[0].transAxes, bbox=props)
    ax[0].tick_params(axis='x', labelrotation=45) 
    plt.tight_layout()
    st.pyplot(fig)

    return ini_value_spy, fin_value_spy, delta_p_spy, ini_value, fin_value, delta_p



def get_metrics(spy_close,sector_dfs, sect_opt):
    ini_value_spy = spy_close['Close'].iloc[0]       
    fin_value_spy = spy_close['Close'].iloc[-1]
    delta_p_spy = round(100*(fin_value_spy-ini_value_spy)/ini_value_spy,2)

    my_df = sector_dfs[sect_opt]
    my_df = my_df[['Date', 'mean']]
    ini_value = my_df.iloc[0,1]
    fin_value = my_df.iloc[-1,1]
    delta_p = round(100*(fin_value-ini_value)/ini_value,2)

    return (ini_value_spy, fin_value_spy, delta_p_spy ), (ini_value, fin_value, delta_p)



def show_sector_metrics(fin_value_spy, delta_p_spy, fin_value, delta_p, sect_opt) :

    colp1, colp2 = st.columns([1,1])
    with colp1:
        st.markdown('---')
        st.markdown("### :blue[S&P500 (SPY)]")        
        st.markdown('---')
        st.metric(f"SPY ", str(fin_value_spy)+" u$s", str(delta_p_spy)+" %")
        st.markdown('---')

    with colp2:
        st.markdown('---')
        st.markdown(f"### :violet[Sector {sect_opt}]")
        st.markdown('---')
        st.metric(f"{sect_opt} (promedio)", str(round(fin_value,2)) +" u$s", str(delta_p)+" %")
        st.markdown('---')
        


def sector_container(companies, sector_dfs, spy_close):

    colx1, colx2, colx3, colx4 = st.columns([2, 6,1,6])
    with colx1:
        sect_opt = sector_opt(companies)
    with colx2:
        tab1, tab2 = st.tabs([f'Spy vs {sect_opt}', f'Spy vs {sect_opt} - variacion %'])
        with tab1:
            plot_sector_vs_spy(sector_dfs, sect_opt, spy_close)
        with tab2:
            plot_sector_vs_spy_delta(spy_close, sector_dfs, sect_opt)    
    with colx4:
        (ini_value_spy, fin_value_spy, delta_p_spy ), (ini_value, fin_value, delta_p) = get_metrics(spy_close,sector_dfs, sect_opt)
        show_sector_metrics(fin_value_spy, delta_p_spy, fin_value, delta_p, sect_opt)


def load_dataframes():
    # ---------------------------------------------------------------------------  
    df = pd.read_csv('./data/tk502.csv')
    companies = pd.read_csv('./data/sp500list.csv')
    spy = pd.read_csv('./data/SPY.csv')
    sector = companies['GICS Sector'].unique().tolist()

    pd.options.mode.chained_assignment = None

    spy_close = spy[["Date", "Close"]]
    spy_close["Date"] =  pd.to_datetime(spy_close["Date"], format="%Y-%m-%d")   

    ticker_by_sector = {}

    for s in sector:
        ticker_by_sector[s] = companies.loc[companies['GICS Sector']==s,'Symbol'].tolist()

    # for s in sector:
    #     st.markdown(f' * {s:} ➡️  {len(ticker_by_sector[s])}')

    sector_dfs = {}

    for s in sector:
        aus = df[ticker_by_sector[s]].copy()
        aus["Date"] = df["Date"]
        aus["Date"] =  pd.to_datetime(aus["Date"], format="%Y-%m-%d")  
        aus['mean'] = aus.iloc[:,1:].mean(axis=1)
        sector_dfs[s] = aus
   

    return df, companies, spy, sector, spy_close, sector_dfs


def date_filter_opt():
    """"
    Retorna un menu desplegable con posibles rangos de fechas
    """
    fechas = ["Último año", "Últimos 5 años", "Últimos 10 años", "Últimos 15 años", "Últimos 23 años"]
    msg = "Seleccione rango de fechas"



    option = st.selectbox(
    msg,
    fechas)

    return option


def get_n_rows(date_filter_opt):
    
    date_opt = {
        "Último año":1
        , "Últimos 5 años":5
        , "Últimos 10 años":10
        , "Últimos 15 años":15
        , "Últimos 23 años":23

    }

    return date_opt[date_filter_opt]



def shorten_df(df, companies, spy, sector, spy_close, sector_dfs,  date_opt):
    ### Nota: esta todo hecho contando como fecha de cuenta del año, diciembre 2022.
    ### Es un poco mas de 1 año    
    fecha_fin = spy_close['Date'].iloc[-1].strftime("%Y-%m-%d")
    if date_opt=="Último año":
        fecha_ini = "2021-12-31"
    elif date_opt=="Últimos 5 años":
        fecha_ini = "2017-12-31"
    elif date_opt=="Últimos 10 años":
        fecha_ini = "2012-12-31"
    elif date_opt=="Últimos 15 años":
        fecha_ini = "2007-12-31"
    elif date_opt=="Últimos 23 años":
        fecha_ini = "2000-01-01"
    else:
        fecha_ini = "2000-01-01"


    df_short = df[df['Date'].between(fecha_ini, fecha_fin)]
    spy_close_short = spy_close[spy_close['Date'].between(fecha_ini, fecha_fin)]
    
    sector_dfs_short = {}
    for s in sector:
        sector_dfs_short[s] = sector_dfs[s][sector_dfs[s]['Date'].between(fecha_ini, fecha_fin)]

    return df_short, spy_close_short, sector_dfs_short
    
    