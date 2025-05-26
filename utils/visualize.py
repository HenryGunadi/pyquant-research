# to import dependecies outside ipynb, select your current python interpreter
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

def plot_RSI(data: pd.DataFrame, rsi_values):
    date_labels = data.index.strftime("%Y-%m-%d").tolist()

    plt.figure(figsize=(14, 8))
    plt.plot(range(len(rsi_values)), rsi_values, label="RSI")

    plt.xticks(ticks=range(len(rsi_values)), labels=date_labels[-len(rsi_values):], rotation=60)
    plt.ylim(0, 100)
    plt.yticks(range(0, 101, 10))

    plt.title("RSI Indicator")
    plt.xlabel("Date")
    plt.ylabel("RSI Value")
    plt.legend()
    plt.tight_layout()
    plt.show()