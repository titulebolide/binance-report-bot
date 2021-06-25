import brb.crypto
import brb.utils
import brb.io
import logging
import conf
import click
import brb
import sys
import traceback


@click.group()
@click.option("--debug/--no-debug", default=False, help="Prints debug data")
def cli(debug):
    """
    Binance Report Bot

    Take a snapshot of your binance wallet, e.g. the current balances and store it for further plotting.
    """
    brb.utils.check_configuration(conf)
    if debug:
        brb.logger.setLevel(logging.DEBUG)


@cli.command(
    "snapshot",
    short_help="Take a snapshot of your wallet",
    help="Take a snapshot of the binance wallet and save it for further plotting",
)
def snapshot():
    crypto_report = brb.crypto.get_report()
    crypto_reports = brb.crypto.save_report(
        crypto_report, brb.crypto.get_previous_reports()
    )
    brb.logger.info("Snapshot saved")


@cli.command(
    "output",
    short_help="Output the previously stored data",
    help="Output the previously stored data with 'snapshot'",
)
@click.option(
    "--quiet/--no-quiet",
    default=False,
    help="Set to true if you don't want to print in the console or display an image",
)
@click.option(
    "-r",
    "--relative/--no-relative",
    default=False,
    help="If the graph should be plotted relative to its initial value",
)
@click.option(
    "-s",
    "--symbol",
    default=conf.CURRENCY,
    help="""The currency the graph will be plotted on.
To plot several symbols on the same graph, separate them by a coma.
If plotting several symbols, the --relative option is enabled.
To plot all symbols, use '*'.
Default : FIAT""",
)
@click.option(
    "-d",
    "--days",
    default=7,
    help="""The number of days over which the graph will be plotted.
If set to 0, the graph will plot all the records.
Default : 7 days""",
)
def output(quiet, relative, symbol, days):
    if symbol == "*":
        symbol = conf.COINS
    else:
        symbol = symbol.split(",")
        for s in symbol:
            assert s in conf.COINS + [conf.CURRENCY]
    if len(symbol) > 1:
        relative = True
    reports = brb.crypto.get_previous_reports()
    if len(reports) == 0:
        msg = "No snapshot in database. Run at least once main.py snapshot"
        figname = None
    else:
        msg = brb.crypto.format_report(reports)
        figname = brb.crypto.plot_symbol(reports, symbol, relative, days)

    brb.io.output(msg, figname, quiet)


if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        brb.logger.error("".join(traceback.format_exception(*sys.exc_info())))
        raise
