import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from src.utils import crisis_dict, crisis_options


def plot_crisis(opt,ax, df, crisis_dict, crisis_options):
    """
    Plotea dos lineas verticales indicando
    - Linea roja, fecha del minimo
    - Linea verde, fecha del maximo

    > opc = Opciones de crisis
    - "Ninguna en particular"
    - "Burbuja dot com"
    - "Burbuja Subprime"
    - "Pandemia Covid"

    > ax = figura donde se deben plotear las lineas
    
    > df = Dataframe conteniendo los precios del indice SP500 (spy)

    > crisis_dict = funcion que carga un dicionario que contiene fecha de inicio y fin de cada crisis

    > crisis_options = funcion que carga las opciones de crisis. Actualmente sin uso   


    """

    # Cargo diccionario de fechas de crisis
    date_dict = crisis_dict()
    
    # Para plotear, se debe seleccionar una crisis (si o si)
    if opt!="Ninguna en particular":
        filter_df= df[df["Date"].between(date_dict[opt][0],date_dict[opt][1])]        
        min_date_dc = filter_df.loc[filter_df['Close'].idxmin(), 'Date']
        max_date_dc = filter_df.loc[filter_df['Close'].idxmax(), 'Date']
        ax.axvline(x=min_date_dc, label="Min", color='red')
        ax.axvline(x=max_date_dc, label="Max", color='green')



def plot_spy(plt_sp500, spy_short, crisis_opt, spy):
    """
    Plotea los datos del ETF que replica el comportamiento del indice SP500.

    > plt_sp500: Booleano que indica si se debe plotear o no

    > spy_short: dataframe con los precios del SPY, afectado por los rangos de fecha del slider de la pag. ppal.

    > crisis_opt: string que indica si se ha seleccionado una crisis

    > spy: dataframe con los precios del SPY, sin afectar por slide

    """

    
    if plt_sp500:
        fig,ax = plt.subplots(figsize=(6, 3))
        g1 = sns.lineplot(x="Date",y="Close", data=spy_short, ax=ax, label="S&P Index (SPY)")    
        # plot_crisis(crisis_opt, ax, spy)
        plot_crisis(crisis_opt,ax, spy, crisis_dict, crisis_options)
        ax.set(title="Evolución del S&P 500")
        ax.set(xlabel="Años", ylabel="Precio cierre")
        # ax.legend()
        # st.pyplot(fig)
        return fig, ax
    else:
        return None, None



def plot_company_or_spy_or_both(plt_company, ticker, sp500_short, spy_short, plt_sp500, crisis_opt, spy):
    """
    De acuerdo a las opciones seleccionadas, plotea el SPY, una accion, o ambos

    > plt_company: booleano, indica si se debe o no plotear la compañia

    > ticker: ticker de la compañia

    > sp500_short:  dataframe con los datos de todas las compañias, afectado por el slide

    > spy_short: dataframe con los datos del Spy, afectado por el slide

    > plt_sp500: indica si se debe plotear el SPY

    > spy: dataframe con los datos del SPY, sin afectar por el slide

    """


    # Si esta habilitada la opcion plt_sp500
    if plt_sp500:
            fig, ax = plot_spy(plt_sp500, spy_short, crisis_opt, spy)
            
    # Si no esta habilitada la opcion plt_sp500, pero si la opcion plt_company
    elif plt_company:
            fig, ax = plt.subplots(figsize=(10, 4))


    if plt_company and ticker!="Only SPY":
        # print(sp500_short.head())
        df_short = sp500_short[["Date", ticker]]
        # print(df_short.tail())

        g2 = sns.lineplot(x="Date",y=ticker, data=sp500_short, ax=ax, label="Ticker: "+ticker)
        if not plt_sp500:
            
            plot_crisis(crisis_opt,ax, spy, crisis_dict, crisis_options)
            ax.set(title="Evolución de "+ticker)
            ax.set(xlabel="Años")
            ax.set(ylabel="Precio cierre")
        else:
            ax.set(title="Evolución del S&P 500 vs "+ticker)
    
    if plt_sp500 or plt_company:
        ax.tick_params(axis='x', labelrotation=45)
        ax.legend()
        st.pyplot(fig)




def subplot_spy_and_company(ticker, crisis_opt, spy_short, sp500_short, spy):
    """
    Subplotear SPY y Compañia, si se ha seleccionado alguna compañia

    > ticker: String, compañia seleccionada
    > crisis_opt: String, crisis seleccionada
    > spy_short: dataframe, contiene los datos del SPY afectados por el slide
    > sp500_short: dataframe, contiene los datos de todas las compañias, afectados por el slide
    > spy: dataframe, contiene los datos del SPY sin afectar por el slide
    
    """

    if ticker!="Only SPY":
        fig, ax = plt.subplots(1,2,figsize=(10, 4))
        g1 = sns.lineplot(x="Date",y="Close", data=spy_short, ax=ax[0], label="S&P Index (SPY)")       
        g2 = sns.lineplot(x="Date",y=ticker, data=sp500_short, ax=ax[1], label="Ticker: "+ticker, color='orange') 
        
        plot_crisis(crisis_opt,ax[0], spy, crisis_dict, crisis_options)
        
        plot_crisis(crisis_opt,ax[1], spy, crisis_dict, crisis_options)
        ax[0].legend()
        ax[1].legend()
        
        # Set tickers a 45°
        for bbx in ax:
            
            bbx.tick_params(axis='x', labelrotation=45)
        
        st.pyplot(fig) 




def plot_zoom_crisis(ticker, crisis_opt, spy, sp500_companies, crisis_dict, crisis_options, plt_zoom, plt_sp500, plt_company):
    """
    Plotea un zoom del SPY y/o una compañia, si se ha seleccionado una crisis economica

    > ticker: string, compañia seleccionada
    > crisis_opt: string, crisis seleccionada
    > spy: dataframe, contiene los datos del SPY sin afectar por el slide
    > sp500_companies: dataframe, contiene los datos de todas las empresas sin afectar por slide
    > crisis_dict: diccionario, contiene las fechas de inicio y fin de las crisis financieras
    > crisis_options: lista, contiene todas las opciones de crisis
    > plt_zoom: booleano, indica si se debe plotear o no un zoom
    > plt_sp500: booleano, indica si se debe o no  plotear el SPY
    > plt_company: booleano, indica si se debe o no plotear la compañia
    
    """

    
    # print("Tciker --> ", ticker)
    if plt_zoom:
        date_dict = crisis_dict()
        crisis_options = crisis_options()

        if plt_sp500:
            fig, ax = plt.subplots()
            spy_filter = spy[spy["Date"].between(date_dict[crisis_opt][0],date_dict[crisis_opt][1])]
            g1 = sns.lineplot(x="Date", y='Close', data=spy_filter, ax = ax, label="S&P Index (SPY)")

        elif plt_company and ticker!="Only SPY":
            fig, ax = plt.subplots()


        if plt_company and ticker!="Only SPY":
            comp_filter = sp500_companies.loc[~sp500_companies[ticker].isna(),["Date",ticker]]
            # print("head --> ", comp_filter.head())
            comp_filter = comp_filter[comp_filter['Date'].between(date_dict[crisis_opt][0],date_dict[crisis_opt][1])]
            # comp_fiter = sp500_companies[sp500_companies['Date'].between(date_dict[crisis_opt][0],date_dict[crisis_opt][1]),[]]
            g2 = sns.lineplot(x="Date", y=ticker, data=comp_filter, ax = ax, label=ticker)

        if plt_sp500 or (plt_company and ticker!="Only SPY"):
            plot_crisis(crisis_opt,ax, spy, crisis_dict, crisis_options)
            ax.legend()
            ax.tick_params(axis='x', labelrotation=45)
            st.pyplot(fig) 