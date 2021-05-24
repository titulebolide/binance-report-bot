import requests
import numpy as np
import conf
import os
import time
import matplotlib.pyplot as plt
import binance


def get_report():
    api = binance.Client(conf.BINANCE_API_KEY, conf.BINANCE_API_SECRET)
    tickers_raw = api.get_symbol_ticker()
    tickers = {'USDT' : 1}
    for t in tickers_raw:
        if t['symbol'].endswith('USDT'):
            tickers[t['symbol'][:-4]] = float(t['price'])
    account = api.get_account()
    total_usdt = 0
    balances = {}
    for balance in account['balances']:
        symbol = balance['asset']
        qty = float(balance["free"]) + float(balance["locked"])
        if qty == 0:
            continue
        balances[symbol] = qty
        if symbol in tickers:
            total_usdt += qty*tickers[symbol]
        else:
            print(f'WARN : Missing symbol {symbol} in binance tickers')

    report_tickers = {}
    all_symbols = list(set(conf.COINS + list(balances.keys())))
    if conf.CURRENCY not in all_symbols and conf.CURRENCY != 'USD':
        all_symbols.append(conf.CURRENCY)
    for symbol in all_symbols:
        if symbol in tickers:
            report_tickers[symbol] = tickers[symbol]
        else:
            print(f'WARN : Missing symbol {symbol} in binance tickers')

    report = {}
    report['total_usdt'] = total_usdt
    report['balances'] = balances
    report['tickers'] = report_tickers
    report['version'] = 2
    return report


def get_currency_change(tickers):
    if conf.CURRENCY == 'USD':
        currency_change = 1 #USD approx USDT
    else:
        currency_change = 0
        if conf.CURRENCY in tickers:
            currency_change = 1/tickers[conf.CURRENCY]
        else:
            print(f'WARN : Missing symbol {conf.CURRENCY} in report')
    return currency_change


def format_report(report):
    msg = "#### Marché actuel:\n"
    currency_change = get_currency_change(report['tickers'])
    for symbol, qty in report['balances'].items():
        value = 0
        ticker = 0
        if symbol in report['tickers']:
            ticker = report['tickers'][symbol]
            value = round(qty*ticker*currency_change,2)
        else:
            print(f'WARN : Missing symbol {symbol} in report')
        if value < 0.1:
            continue
        msg += f"- **{symbol}**  *({ticker} {conf.CURRENCY_SYMBOL})* : {value} {conf.CURRENCY_SYMBOL}\n"

    total = round(report['total_usdt']*currency_change,2)
    msg += f"\n**Total** : {total} {conf.CURRENCY_SYMBOL}\n"
    return msg


def get_previous_reports():
    if os.path.exists('db/crypto.npy'):
        reports = np.load('db/crypto.npy', allow_pickle=True).tolist()
        return reports
    else:
        return []


def save_report(report, old_reports):
    report["time"] = int(time.time())
    old_reports.append(report)
    np.save('db/crypto.npy', old_reports, allow_pickle=True)
    return old_reports


def plot_reports(reports):
    X,Y = [],[]
    for report in reports:
        currency_change = get_currency_change(report['tickers'])
        Y.append(report['total_usdt']*currency_change)
        X.append(report['time'])

    plt.plot(X,Y)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid()
    figname = "db/value.png"
    plt.savefig(figname)
    return figname
