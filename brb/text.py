import numpy as np
import brb.conf as conf

def format_report(reports):
    msg = "**Current market**:"

    currency_change = 1 / reports[-1]["tickers"][conf.CURRENCY]
    for symbol, qty in reports[-1]["balances"].items():
        if symbol not in reports[-1]["tickers"]:
            continue
        ticker = reports[-1]["tickers"][symbol]
        value_usd = qty * ticker
        if value_usd < 0.1:
            continue
        value = round(value_usd * currency_change, 2)
        msg += f"\n- **{symbol}**  *(@ ${ticker})* : {value} {conf.CURRENCY_SYMBOL}"

    total = reports[-1]["total_usdt"] * currency_change
    msg += f"\n\n**Total** : {round(total,2)} {conf.CURRENCY_SYMBOL}"

    all_ts = np.array([report["time"] for report in reports])
    current_ts = reports[-1]["time"]
    for pos in conf.DIFFS_POSITIONS:
        older_than_pos = np.where(all_ts < current_ts - pos["ts_delta"])[0]
        if len(older_than_pos) == 0:
            # if there is no record old enough
            continue
        # taking the report at the earlier timestamp that is
        # older than current_ts - pos['ts_delta']
        report = reports[older_than_pos[-1]]
        if not conf.CURRENCY in report["tickers"]:
            continue
        pos_report_total = report["total_usdt"] / report["tickers"][conf.CURRENCY]
        diff = total - pos_report_total
        diff_sign = "+" if diff > 0 else ""
        text = pos["text"]
        msg += f"\n- Since last {text} : {diff_sign}{round(diff,2)} {conf.CURRENCY_SYMBOL} ({diff_sign}{round(diff/pos_report_total*100,2)}%)"

    return msg
