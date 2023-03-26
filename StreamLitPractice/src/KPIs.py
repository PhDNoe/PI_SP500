from src.utils import get_spy_difference, get_company_difference
import streamlit as st



def spy_diff_kpi_movil(spy_short, crisis_dict):
    """
    Calcula la evolucion del precio del SPY en el rango de tiempo especificado por el slide

    name = S&P500 (SPY)
    value = precio de cierre, fecha = fecha superior del rango seleccionado
    delta = variacion porcentual del valor, en el rango de tiempo especificado por el slide

    > spy_short: dataframe, contiene los precios del SPY afectado por el slide
    > crisis_dict: diccionario, contiene las fechas de inicio y fin de las crisis
    """
    
    spy_ini, spy_fin, delta_spy, spy_ini_date, spy_fin_date = get_spy_difference(spy_short,spy_short, "Ninguna en particular", crisis_dict)
    

    name = "S&P500(SPY) "
    value = str(round(spy_fin,2))+ " u$s"
    delta = str(delta_spy) + " %"

    kpi = st.metric(name, value,delta)
    return kpi




def company_diff_kpi_movil(sp500_short, crisis_dict, tk_opt):
    """
    Calcula la evolucion del precio de la compañia seleccionada en el rango de tiempo especificado por el slide
    
    name = Ticker de la compañia
    value = precio de cierre, fecha = fecha superior del rango seleccionado
    delta = variacion porcentual del valor, en el rango de tiempo especificado por el slide

    > sp500_short: dataframe, contiene los datos de todas las empresas. Afectado por el slide
    > crisis_dict: diccionario, contiene las fechas de inicio y fin de las crisis
    > tk_opt: string, ticker de la empresa seleccionada

    """

    df_ini, df_fin, delta_df, df_ini_date, df_fin_date = get_company_difference(sp500_short, sp500_short, tk_opt, "Ninguna en particular", crisis_dict)

    if tk_opt!="Only SPY":
        name = tk_opt
        if df_fin is not None and delta_df is not None:            
            value = str(round(df_fin,2)) + " u$s"
            delta = str(delta_df) + " %"
        else:
            value = None
            delta = None

        kpi = st.metric(name, value,delta)
    else:
        name = "Sin seleccion"
        value = None
        delta = None


    return kpi