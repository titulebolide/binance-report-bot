import requests
import numpy as np
import conf
from oauth2client.service_account import ServiceAccountCredentials
import os
import time
import matplotlib.pyplot as plt
import binance

def get_report(st):
    api = binance.Client(conf.BINANCE_API_KEY, conf.BINANCE_API_SECRET)
    account = api.get_account()
    total_eur = 0
    symbol_eur_value = {}
    for balance in account['balances']:
        symbol = balance['asset']
        qty = float(balance["free"]) + float(balance["locked"])
        if qty == 0:
            continue
        qty_eur = qty*st.getTicker(symbol)
        symbol_eur_value[symbol] = qty_eur
        total_eur += qty_eur

    report = {}
    report['total'] = total_eur
    report['value_eur'] = symbol_eur_value
    return report

def format_report(st, report):
    msg = "#### Marché actuel:\n"

    for symbol, value in report['value_eur'].items():
        msg += "- **{}**  *({} €)* : {} €\n".format(symbol, st.getTicker(symbol), round(value,2))

    msg+="\n**Total** : {}€"
    if 'profits' in report:
        msg+="\n<font color='{}'>**Profit** : {} €</font> \n***\n\n".format(
            round(report['total'],2),
            "#9dc209" if report['profits'] > 0 else "#b22222",
            round(report['profits'],2)
        )
    return msg


def get_previous_reports():
    if os.path.exists('db/crypto.npy'):
        reports = np.load('db/crypto.npy', allow_pickle=True).tolist()
        return reports
    else:
        return []

def save_report(report, old_reports):
    old_reports.append({
        "time": time.time(),
        "report": report
    })
    np.save('db/crypto.npy', old_reports, allow_pickle=True)
    return old_reports

def plot_reports(reports):
    X,Y = [],[]
    for report in reports:
        X.append(report['time'])
        Y.append(report['report']['total'])
    plt.plot(X,Y)
    plt.xlabel('Time')
    plt.ylabel('Profit')
    plt.grid()
    figname = "db/profit.png"
    plt.savefig(figname)
    return figname
