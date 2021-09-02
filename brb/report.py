import os
import time
import requests
import binance
import numpy as np
import brb
import brb.conf as conf


def build_ticker(all_symbols, tickers_raw):
    backup_coins = ["BTC", "ETH", "BNB"]
    tickers = {"USDT": 1, "USD": 1}
    tickers_raw = {t["symbol"]: float(t["price"]) for t in tickers_raw}
    failed_coins = []

    for symbol in set(backup_coins + all_symbols):
        success = False
        for stable in ("USDT", "BUSD", "USDC", "DAI"):
            pair = symbol + stable
            if pair in tickers_raw:
                tickers[symbol] = tickers_raw[pair]
                success = True
                break
        if not success:
            failed_coins.append(symbol)

    for symbol in failed_coins:
        success = False
        for b_coin in backup_coins:
            pair = symbol + b_coin
            if pair in tickers_raw:
                tickers[symbol] = tickers_raw[pair] * tickers[b_coin]

    return tickers


def get_report():
    api = binance.Client(
        conf.BINANCE_API_KEY,
        conf.BINANCE_API_SECRET,
        tld = conf.TLD
    )

    account = api.get_account()
    account_symbols = []
    balances = {}
    for balance in account["balances"]:
        symbol = balance["asset"]

        if symbol.startswith("LD"):
            # skip the coins in binance saving
            # (see https://github.com/titulebolide/binance-report-bot/issues/5)
            continue

        qty = float(balance["free"]) + float(balance["locked"])
        if qty != 0:
            account_symbols.append(symbol)
            balances[symbol] = qty

    all_symbols = list(set(conf.COINS + account_symbols))
    if conf.CURRENCY == "EUR":
        all_symbols.append("EUR")
    tickers_raw = api.get_symbol_ticker()
    tickers = build_ticker(all_symbols, tickers_raw)
    if conf.CURRENCY not in ("USD", "EUR"):
        ticker = (
            1
            / requests.get(
                "https://openexchangerates.org/api/latest.json?app_id="
                + conf.OER_APP_ID
            ).json()["rates"][conf.CURRENCY]
        )
        tickers[conf.CURRENCY] = ticker

    brb.logger.debug(all_symbols)
    brb.logger.debug(tickers)

    total_usdt = 0
    for symbol in account_symbols:
        if symbol not in tickers:
            continue
        total_usdt += balances[symbol] * tickers[symbol]

    report = {}
    report["total_usdt"] = total_usdt
    report["balances"] = balances
    report["tickers"] = tickers
    return report


def get_previous_reports():
    if os.path.exists("db/crypto.npy"):
        reports = np.load("db/crypto.npy", allow_pickle=True).tolist()
        return reports
    else:
        return []


def save_report(report, old_reports):
    report["time"] = int(time.time())
    old_reports.append(report)
    np.save("db/crypto.npy", old_reports, allow_pickle=True)
    return old_reports
