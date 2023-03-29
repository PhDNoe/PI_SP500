import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.page3_src.p3_functions import date_filter_opt, get_n_rows,shorten_df, sector_container, load_dataframes, inflation_metrics, inflation_table
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# page layout
st.set_page_config(layout="wide")

date_opt = date_filter_opt()
color_n_rows = get_n_rows(date_opt)


inflation_metrics(color_n_rows)
with st.expander("Ver tabla de inflación"):
    inflation_table(color_n_rows)


df, companies, spy, sector, spy_close, sector_dfs = load_dataframes()
df_short, spy_close_short, sector_dfs_short = shorten_df(df, companies, spy, sector, spy_close, sector_dfs, date_opt)


container2 = st.container()
with container2:
    sector_container(companies, sector_dfs_short, spy_close_short)




