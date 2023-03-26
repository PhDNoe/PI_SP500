import seaborn as sns

import matplotlib.pyplot as plt

def plot_sp500(df):
    
    fig, ax = plt.subfigures(figsize=(8,4))
    g1 = sns.lineplot(x="Date",y="Close", data=df, ax=ax, label="S&P Index (SPY)")   
    return fig, ax


