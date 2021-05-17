import requests
import numpy as np
import conf
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import time
import matplotlib.pyplot as plt
import binance

def get_report(st):

    sheet_data = np.array(
        gspread.service_account(
            filename=conf.GOOGLE_TOKEN_FILE
        ).open_by_key(conf.SHEET_ID).get_worksheet(0).get('1:3')
    )

    cryptos = set(sheet_data[0,2:])

    symbol_eur_value = {}
    for col in range(2, sheet_data.shape[1]):
        symbol = sheet_data[0,col]
        quantity = float(sheet_data[2,col])
        ticker = st.getTicker(symbol)
        if symbol in symbol_eur_value:
            symbol_eur_value[symbol] += ticker*quantity
        else:
            symbol_eur_value[symbol] = ticker*quantity

    report = {}
    report['total'] = sum(symbol_eur_value.values())
    report['profits'] = report['total'] + float(sheet_data[2,1])
    report['value_eur'] = symbol_eur_value
    return report

def get_report_binance(st):
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
