import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.page2_src.p2_functions import highlight_columns, load_inflation,inflation_container, sector_container, load_dataframes
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# page layout
st.set_page_config(layout="wide")


# Contenedor de inflacion
container1 = st.container()
with container1:
    inflation_container()


df, companies, spy, sector, spy_close, sector_dfs = load_dataframes()
container2 = st.container()
with container2:
    sector_container(companies, sector_dfs, spy_close)
