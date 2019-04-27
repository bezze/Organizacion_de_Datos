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
    fig, ax = plt.subplots(1, 1)
    counts = pd.value_counts(auctions.device_id)
    np.log10(counts.reset_index().device_id).plot.line(ax=ax, marker='o', ms=1)
    ax.set_title('Cantidad de subastas por device_id (ordenado)')
    ax.set_xlabel('device_id (ordenado)')
    ax.set_ylabel('Nº de subastas ($log_{10}$)')
    # plt.show()


def ocurrencias_por_dia_top_5():
    n = 5
    counts = pd.value_counts(auctions.device_id)
    top_n = list(counts[:n].keys())
    filt = [auctions.device_id == i for i in top_n]
    for i in range(len(filt) - 1):
        filt[0] ^= filt[i + 1]
    days = auctions.date.apply(lambda x: x.day)
    auctions['days'] = days
    auctions_filt = auctions[filt[0]]

    df = auctions_filt.pivot_table(
        index=['days'],
        aggfunc={'device_id': np.count_nonzero},
        columns="device_id")

    fig, ax = plt.subplots(1, 1)
    df.plot.bar(ax=ax)
    ax.set_title('Ocurrencias por dia (top 5)')
    ax.set_xlabel('Dia')
    ax.set_ylabel('Ocurrencias')
    # plt.show()


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
    # plt.show()


def cantidad_de_subastas_por_hora_del_dia_todos():

    daymap = {1: "Lunes", 2: "Martes", 3: "Miercoles", 4: "Jueves",
        5: "Viernes", 6: "Sábado", 7: "Domingo"}

    auctions['hour_series'] = auctions.date.apply(lambda x: x.hour)
    auctions['day_of_week'] = auctions.date.apply(lambda x: (x.day, x.isoweekday()))

    df2 = auctions.pivot_table(index=['hour_series', 'day_of_week'], aggfunc={'device_id': np.count_nonzero}).unstack()
    df4 = df2.reset_index().device_id
    new_names = { i:daymap[i[1]]+" "+str(i[0]) for i in df4.columns }
    named_df = df4.rename(columns=new_names)

    fig, ax = plt.subplots(1,1); named_df.plot.line(ax=ax)
    ax.set_xlabel('Horas'); ax.set_ylabel('Ocurrencias'); ax.set_title('Cantidad de subastas por hora de cada dia');
    plt.legend(fontsize='small')
    fig.tight_layout()
    plt.show()


# cantidad_de_subastas_por_device_id_ordenado()
# ocurrencias_por_dia_top_5()
# subastas_promedio_por_hora_del_dia_top_5()
# cantidad_de_subastas_por_hora_del_dia_todos()


"""
CLICKS
"""
