"""
oemof application for research project quarree100.

Some parts of the code are adapted from
https://github.com/oemof/oemof-examples
-> excel_reader

SPDX-License-Identifier: GPL-3.0-or-later
"""

import oemof.outputlib as outputlib
import pandas as pd
import os
import config as cfg
from matplotlib import pyplot as plt


def plot_buses(res=None, es=None):

    l_buses = []

    for n in es.nodes:
        type_name =\
            str(type(n)).replace("<class 'oemof.solph.", "").replace("'>", "")
        if type_name == "network.Bus":
            l_buses.append(n.label)

    for n in l_buses:
        bus_sequences = outputlib.views.node(res, n)["sequences"]
        bus_sequences.plot(kind='line', drawstyle="steps-mid", subplots=False,
                           sharey=True)
        plt.show()


def plot_trans_invest(res=None, es=None):

    l_transformer = []

    for n in es.nodes:
        type_name =\
            str(type(n)).replace("<class 'oemof.solph.", "").replace("'>", "")
        if type_name == "network.Transformer":
            l_transformer.append(n.label)

    p_trans_install = []

    for q in l_transformer:
        p_install = outputlib.views.node(res, q)["scalars"][0]
        p_trans_install.append(p_install)

    # plot the installed Transformer Capacities
    y = p_trans_install
    x = l_transformer
    width = 1/2
    plt.bar(x, y, width, color="blue")
    plt.ylabel('Installierte Leistung [kW]')
    plt.show()


def plot_storages_soc(res=None, es=None):

    l_storages = []

    for n in es.nodes:
        type_name =\
            str(type(n)).replace("<class 'oemof.solph.", "").replace("'>", "")
        if type_name == "components.GenericStorage":
            l_storages.append(n.label)

    for n in l_storages:
        soc_sequences = outputlib.views.node(res, n)["sequences"]
        soc_sequences = soc_sequences.drop(soc_sequences.columns[[0, 2]], 1)
        soc_sequences.plot(kind='line', drawstyle="steps-mid", subplots=False,
                           sharey=True)
        plt.show()


def plot_storages_invest(res=None, es=None):

    l_storages = []

    for n in es.nodes:
        type_name =\
            str(type(n)).replace("<class 'oemof.solph.", "").replace("'>", "")
        if type_name == "components.GenericStorage":
            l_storages.append(n.label)

    c_storage_install = []

    for n in l_storages:
        c_storage = outputlib.views.node(res, n)["scalars"][0]
        c_storage_install.append(c_storage)

    # plot the installed Storage Capacities
    plt.bar(l_storages, c_storage_install, width=0.5, color="blue")
    plt.ylabel('Kapazität [kWh]')
    plt.show()


def export_excel(res=None, es=None):

    l_buses = []

    for n in es.nodes:
        type_name =\
            str(type(n)).replace("<class 'oemof.solph.", "").replace("'>", "")
        if type_name == "network.Bus":
            l_buses.append(n.label)

    l_transformer = []

    for n in es.nodes:
        type_name =\
            str(type(n)).replace("<class 'oemof.solph.", "").replace("'>", "")
        if type_name == "network.Transformer":
            l_transformer.append(n.label)

    l_storages = []

    for s in es.nodes:
        type_name =\
            str(type(s)).replace("<class 'oemof.solph.", "").replace("'>", "")
        if type_name == "components.GenericStorage":
            l_storages.append(s.label)

    df_series = pd.DataFrame()

    for n in l_buses:
        bus_sequences = outputlib.views.node(res, n)["sequences"]
        df_series = pd.concat([df_series, bus_sequences], axis=1)

    for n in l_storages:
        soc_sequences = outputlib.views.node(res, n)["sequences"]
        df_series = pd.concat([df_series, soc_sequences], axis=1)

    c_storage_install = []

    for n in l_storages:
        c_storage = outputlib.views.node(res, n)["scalars"][0]
        c_storage_install.append(c_storage)

    p_trans_install = []

    for q in l_transformer:
        p_install = outputlib.views.node(res, q)["scalars"][0]
        p_trans_install.append(p_install)

    df_invest_ges = pd.DataFrame(
        [p_trans_install+c_storage_install],
        columns=l_transformer+l_storages)

    # the result_gesamt df is exported in excel
    path_to_results = os.path.join(os.path.expanduser("~"),
                                   cfg.get('paths', 'results'))
    filename = 'results.xlsx'
    with pd.ExcelWriter(os.path.join(path_to_results, filename)) as xls:
        df_series.to_excel(xls, sheet_name='Timeseries')
        df_invest_ges.to_excel(xls, sheet_name='Invest')
