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

# auctions_dfile = Auctions.load(name="auctions.csv")
auctions_dfile = DataFile.load(name="auctions.pickle")
auctions = auctions_dfile.df

# events_dfile = Events.load(name="events.csv")
events_dfile = Events.load(name="events.pickle")
events = events_dfile.df

installs_dfile = Installs.load(name="installs.csv")
installs = installs_dfile.df


def finger_1a(n, show=False):
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

    df = auctions_filt.pivot_table(index=["hour_series", 'days'], aggfunc={'date': np.count_nonzero}, columns="device_id").unstack('hour_series').mean().unstack('device_id')
    df=df.reset_index()
    del df['level_0']

    if show:
        fig, ax = plt.subplots(1,1)
        plt.plot(df.values[:,0], df.values[:,1:])
        # auctions_filt.pivot_table(index=["hour_series"], aggfunc=np.count_nonzero, columns="device_id", values="date").plot.bar(ax=ax)
        ax.set_title('Subastas por hora del día')
        ax.set_xlabel('Horas')
        ax.set_ylabel('Ocurrencias')
        plt.show()

    return auctions_filt


def finger_1b():
    clicks=None
    clicks_p_hour = clicks.groupby("hour").agg({"ref_hash": np.count_nonzero})


def more_eventful_applications(n, show=False):
    grouped_apps = events.groupby("application_id")
    sort_grouped_apps = grouped_apps.event_id.count().sort_values(ascending=False)[:n]
    if show:
        sort_grouped_apps.plot.bar()
        plt.show()
    return sort_grouped_apps


def eventful_applications_and_user_prop(n, show=False):
    app_hash = events.groupby(['application_id', 'ref_hash'])['ref_hash'].count()
    df2=app_hash.unstack('ref_hash').fillna(0)
    df2['total']=df2.agg(np.sum, axis=1)
    df3=df2.sort_values(by='total', ascending=False)
    if show:
        df3[:n].plot.bar(stacked=True)
        plt.show()
    return df3[:n]


def topNapps_with_topMusers(N,M):
    df = eventful_applications_and_user_prop(N).astype(np.float32)
    total = df['total'].copy()
    del(df['total'])
    most_eventful_users=df.agg(np.sum, axis=0).sort_values(ascending=False)[:M].keys()
    the_rest = total - df[most_eventful_users].agg(np.sum, axis=1)
    df['rest'] = the_rest

    fig, axes = plt.subplots(2, 1)

    color_dict = {k: '#2f3da8' for k in most_eventful_users}
    color_dict['rest'] = '#8c5926'
    users_plus_rest = list(most_eventful_users) + ['rest']
    ax1 = df[users_plus_rest].plot.bar(stacked=True, ax=axes[0], label=False, color=[color_dict[x] for x in users_plus_rest])
    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend([handles[0],handles[-1]], [f'Top {M}','Rest'])
    ax1.set_title(f'Top {N} aplicaciones con mas eventos (Top {M} azul ref_hash)')
    ax1.set_ylabel('Nº Eventos')

    color_dict = {k: i for k, i in zip(most_eventful_users, colorcet.glasbey)}
    ax2 = df[list(most_eventful_users)].plot.bar(stacked=True, ax=axes[1], color=[color_dict[x] for x in most_eventful_users])
    ax2.get_legend().set_visible(False)
    ax2.set_ylabel('Nº Eventos')
    ax2.set_title('Los colores representan diferentes ref_hash')
    fig.tight_layout()
    return df


def events_from_apps_and_installations(show=False):
    ins_ev = installs.join(events, how='inner', on='application_id', rsuffix='_ins')
    ins_ev_appid = ins_ev.groupby('application_id')
    ev_appid = events.groupby('application_id')
    print('Total de aplicaciones: ', len(events.application_id.unique()))
    print('Aplicaciones que resultan en instalaciones: ', len(ins_ev.application_id.unique()))
    if show:
        # fig, ax = plt.subplots(2,1)
        # ax[0] = ev_appid.agg({'ref_hash': np.count_nonzero}).plot.bar(ax=ax[0])
        fig, ax = plt.subplots(1,1)
        ax = ins_ev_appid.agg({'ref_hash': np.count_nonzero}).plot.bar(ax=ax)
        plt.show()

# pd.merge(events, installs[pd.notnull(installs.event_uuid)], on='event_uuid')
