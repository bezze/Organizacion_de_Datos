#!/usr/bin/env python3
from collections import namedtuple
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import colorcet
from pandas.plotting import register_matplotlib_converters
import seaborn as sns

from src.data_file import DataFile, Auctions, Events, Installs

register_matplotlib_converters()

"""
AUCTIONS
"""
# auctions_dfile = Auctions.load(name="auctions.csv")
auctions_dfile = DataFile.load(name="auctions.pickle")
auctions = auctions_dfile.df


def cantidad_de_subastas_por_device_id_ordenado():
    pass


def ocurrencias_por_dia_top_5():
    pass


def subastas_promedio_por_hora_del_dia_top_5():
    n = 5
    counts = pd.value_counts(auctions.device_id)
    top_n = list(counts[:n].keys())
    filt = [auctions.device_id == i for i in top_n]
    for i in range(len(filt) - 1):
        filt[0] ^= filt[i + 1]
    hours = auctions.date.apply(lambda x: x.hour)
    days = auctions.date.apply(lambda x: x.day)
    auctions['hour_series'] = hours
    auctions['days'] = days
    auctions_filt = auctions[filt[0]]

    df = auctions_filt.pivot_table(
        index=["hour_series", 'days'],
        aggfunc={'date': np.count_nonzero},
        columns="device_id").unstack('hour_series').mean().unstack('device_id')
    df = df.reset_index()
    del df['level_0']

    fig, ax = plt.subplots(1, 1)
    plt.plot(df.values[:, 0], df.values[:, 1:])
    # auctions_filt.pivot_table(index=["hour_series"], aggfunc=np.count_nonzero, columns="device_id", values="date").plot.bar(ax=ax)
    ax.set_title('Subastas por hora del día')
    ax.set_xlabel('Horas')
    ax.set_ylabel('Ocurrencias')
    plt.show()


def cantidad_de_subastas_por_hora_del_dia_todos():
    pass


"""
CLICKS
"""
