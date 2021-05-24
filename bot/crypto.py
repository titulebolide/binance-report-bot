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
    tickers = {'USDT' : 1, 'USD' : 1}
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

    all_symbols = list(set(conf.COINS + list(balances.keys()) + [conf.CURRENCY]))
    report_tickers = {symbol : get_ticker(tickers, symbol) for symbol in all_symbols}

    report = {}
    report['total_usdt'] = total_usdt
    report['balances'] = balances
    report['tickers'] = report_tickers
    report['version'] = 2
    return report


def get_ticker(tickers, symbol):
    ticker = 0
    if symbol in tickers:
        ticker = tickers[symbol]
    else:
        print(f'WARN : Missing symbol {symbol}')
    return ticker


def get_currency_change(tickers):
    ticker = get_ticker(tickers, conf.CURRENCY)
    if ticker == 0:
        return 0
    return 1/ticker


def format_report(report):
    msg = "#### Marché actuel:\n"
    currency_change = 1/get_currency_change(report['tickers'])
    for symbol, qty in report['balances'].items():
        ticker = get_ticker(report['tickers'], symbol)
        value = round(qty*ticker*currency_change,2)
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


def plot_symbol(reports, symbol):
    plt.figure()
    X,Y = [],[]
    for report in reports:
        ticker = get_ticker(report['tickers'], symbol)
        Y.append(report['total_usdt']/ticker)
        X.append(report['time'])
    plt.plot(X,Y)
    plt.xlabel('Time (s)')
    plt.ylabel(f'Value ({symbol})')
    plt.grid()
    figname = f"db/quantity_{symbol}.png"
    plt.savefig(figname)
    return figname
