import streamlit as st

# page layout
st.set_page_config(layout="wide")

st.header("📈 Factibilidad de cartera de inversión")

st.markdown("### Empresa solicitante: :blue[Ficticia Conservadora (F.C)]")
st.markdown("---")
st.markdown("#### La empresa Ficticia Conservadora  ha solicitado una recomendación de cartera de inversión.")
a = """
> * La empresa, una startup en crecimiento, desea invertir un capital excedente.
> * Acepta correr un riesgo mínimo a cambio de una tasa de retorno superior a la tasa de inflación
de Estados Unidos de los ultimos 5 años.
> * Su horizonte de inversión es a mediano/largo plazo, con una estancia mínima de 2 años.

"""
st.markdown(a)


st.markdown('---')
st.markdown('#### Contenido del informe: ')

b="""
* 📈 :violet[Análisis general:] Dashboard interactivo mostrando evolución del índice S&P500 durante 
los últimos 23 años y de las compañías que lo componen.
    - 🗓 Fitros de fechas
    - 🫧 Indicadores gráficos de 3 crisis económicas:
        - 🌐 Burbuja dot com  
        - 🏠 Burbuja de hipotecas subprime
        - 🦠 Pandemia Covid-19  

"""

c="""
* 📈 :violet[Análisis descriptivo y estadístico por sectores:] Dashboard interactivo mostrando la evolución de los últimos 
23 años de los distintos sectores
    - 🗓  Filtro de fechas
    - 📈 Datos de inflación anual y acumulada
"""


d="""
* 📈 :violet[Análisis descriptivo y estadístico de las empresas seleccionadas:] Dashboard interactivo mostrando la evolución de los últimos 
5 años de las distintas empresas
    - 📈 Ganancia porcentual por empresa
    - 📈 Datos de inflación anual y acumulada
    - 📈 Fundamentales de las empresas
    
"""


e = """

* 📈 :violet[Análisis técnico de las compañias recomendadas]: Dashboard interactivo mostrando los principales 
indicadores técnicos para analizar posibles zonas de compra.

    Indicadores disponibles:
    - 📉 Medias moviles de 50 y 100 días
    - 📉 Índice de fuerza relativa (RSI)


"""



f = """

* 📈 :violet[Conclusiones y recomendación final]:


"""

st.markdown(b)
st.markdown(c)
st.markdown(d)
st.markdown(e)
st.markdown(f)
st.markdown('---')

