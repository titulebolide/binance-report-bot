import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np
import time


def graph_report(reports, symbols, relative, days, graph_type, ref_currency):
    plt.clf()
    plt.close()
    if len(symbols) < 10:
        plt.figure()
    else:
        plt.figure(figsize=(10, 6))

    min_timestamp = 0
    if days != 0:
        min_timestamp = time.time() - days * 24 * 60 * 60

    nb_plot = 0
    for symbol in symbols:
        X, Y = [], []
        for report in reports:
            if report["time"] < min_timestamp:
                continue  # skip if too recent
            if symbol not in report["tickers"]:
                brb.logger.debug(f"{symbol} has no price in the report with timestamp {report["time"]}")
                continue
            ticker = report["tickers"][symbol]
            if ticker == 0:
                brb.logger.debug(f"{symbol} has an invalid price in the report with timestamp {report["time"]}")
                continue

            y = None
            if graph_type == "amount":
                y = report["total_usdt"] / ticker
            elif graph_type == "price":
                ref_currency_ticker = 1
                if ref_currency not in ("USD", "USDT"):
                    if ref_currency not in report["tickers"]:
                        continue
                    ref_currency_ticker = report["tickers"][ref_currency]
                    if ref_currency_ticker == 0:
                        continue
                y = ticker / ref_currency_ticker
            if y is None:
                continue

            Y.append(y)
            X.append(dt.datetime.fromtimestamp(report["time"]))
            nb_plot += 1

        if relative:
            Y = np.array(Y)
            Y = (Y / Y[0] - 1) * 100
        plt.plot(X, Y, label=symbol)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M"))
    plt.setp(plt.xticks()[1], rotation=15)
    if graph_type == "amount":
        if relative:
            plt.ylabel("Relative evolution of amount (%)")
            plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
        else:
            label = "Amount"
            label += f" ({symbols[0]})" if len(symbols) == 1 else ""
            plt.ylabel(label)
    elif graph_type == "price":
        if relative:
            plt.ylabel(f"Relative evolution of price in {ref_currency} (%)")
        else:
            plt.ylabel(f"Price in {ref_currency}")
    plt.grid()
    figname = f"db/quantity_{symbol}.png"
    plt.savefig(figname)
    return figname, nb_plot
