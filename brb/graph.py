import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np
import time


def plot_symbol(reports, symbols, relative, days):
    def Y_getter(report, symbol):
        if symbol not in report["tickers"]:
            return
        ticker = report["tickers"][symbol]
        if ticker == 0:
            return
        return report["total_usdt"] / ticker
    return plot_report_data_time(Y_getter, reports, symbols, relative, days)

def plot_tickers(reports, symbols, relative, days):
    def Y_getter(report, symbol):
        if symbol not in report["tickers"]:
            return
        ticker = report["tickers"][symbol]
        if ticker == 0:
            return
        return ticker
    return plot_report_data_time(Y_getter, reports, symbols, relative, days)

def plot_report_data_time(Y_getter, reports, symbols, relative, days):
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

            y = Y_getter(report, symbol)
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
    if relative:
        plt.ylabel("Relative profit (%)")
        plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
    else:
        label = "Amount"
        label += f" ({symbols[0]})" if len(symbols) == 1 else ""
        plt.ylabel(label)
    plt.grid()
    figname = f"db/quantity_{symbol}.png"
    plt.savefig(figname)
    return figname, nb_plot
