import requests
import numpy as np
import conf
import os
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import binance


def build_ticker(all_symbols, tickers_raw):
    backup_coins = ['BTC', 'ETH', 'BNB']
    tickers = {'USDT' : 1, 'USD' : 1}
    tickers_raw = {t['symbol']:float(t['price']) for t in tickers_raw}
    failed_coins = []

    for symbol in set(backup_coins + all_symbols):
        success = False
        for stable in ('USDT', 'BUSD', 'USDC', 'DAI'):
            pair = symbol+stable
            if pair in tickers_raw:
                tickers[symbol] = tickers_raw[pair]
                success = True
                break
        if not success:
            failed_coins.append(symbol)

    for symbol in failed_coins:
        success = False
        for b_coin in backup_coins:
            pair = symbol+b_coin
            if pair in tickers_raw:
                tickers[symbol] = tickers_raw[pair]*tickers[b_coin]

    return tickers


def get_report(debug):
    api = binance.Client(conf.BINANCE_API_KEY, conf.BINANCE_API_SECRET)

    account = api.get_account()
    account_symbols = []
    balances = {}
    for balance in account['balances']:
        symbol = balance['asset']

        if symbol.startswith('LD'):
            # skip the coins in binance saving
            # (see https://github.com/titulebolide/binance-report-bot/issues/5)
            continue

        qty = float(balance["free"]) + float(balance["locked"])
        if qty != 0:
            account_symbols.append(symbol)
            balances[symbol] = qty

    all_symbols = list(set(conf.COINS + account_symbols))
    if conf.CURRENCY == "EUR":
        all_symbols.append('EUR')
    tickers_raw = api.get_symbol_ticker()
    tickers = build_ticker(all_symbols, tickers_raw)
    if conf.CURRENCY not in ('USD', 'EUR'):
        ticker = 1/requests.get(
            "https://openexchangerates.org/api/latest.json?app_id="+conf.OER_APP_ID
        ).json()['rates'][conf.CURRENCY]
        tickers[conf.CURRENCY] = ticker

    if debug:
        print(all_symbols, tickers, sep="\n"*2, end='\n'*2)


    total_usdt = 0
    for symbol in account_symbols:
        total_usdt += balances[symbol]*tickers[symbol]

    report = {}
    report['total_usdt'] = total_usdt
    report['balances'] = balances
    report['tickers'] = tickers
    return report


def format_report(report):
    msg = "**Current market**:\n\n"
    currency_change = 1/report['tickers'][conf.CURRENCY]
    for symbol, qty in report['balances'].items():
        ticker = report['tickers'][symbol]
        value = round(qty*ticker*currency_change,2)
        if value < 0.1:
            continue
        msg += f"- **{symbol}**  *({ticker} $)* : {value} {conf.CURRENCY_SYMBOL}\n"

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


def plot_symbol(reports, symbols, relative, days):

    plt.clf()
    plt.close()
    plt.figure()

    min_timestamp = 0
    if days != 0:
        min_timestamp = time.time() - days*24*60*60

    for symbol in symbols:
        X,Y=[],[]
        for report in reports:
            if report['time'] < min_timestamp:
                continue # skip if too recent
            ticker = report['tickers'][symbol]
            if ticker == 0:
                continue
            Y.append(report['total_usdt']/ticker)
            X.append(dt.datetime.fromtimestamp(report['time']))
        if relative:
            Y = np.array(Y)
            Y = (Y/Y[0] - 1) * 100
        plt.plot(X,Y, label=symbol)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
    plt.setp(plt.xticks()[1], rotation = 15)
    if relative:
        plt.ylabel("Relative profit (%)")
        plt.legend()
    else:
        label = "Amount"
        label += f" ({symbols[0]})" if len(symbols) == 1 else ""
        plt.ylabel(label)
    plt.grid()
    figname = f"db/quantity_{symbol}.png"
    plt.savefig(figname)
    return figname
