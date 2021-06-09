import bot
import conf
import click


@click.group()
def cli():
    """
    Take a snapshot of your binance wallet, e.g. the current balances and store it for further plotting.
    """
    bot.utils.check_configuration(conf)


@cli.command(
    'snapshot',
    short_help = "Take a snapshot of your wallet",
    help = "Take a snapshot of the binance wallet and save it for further plotting"
)
@click.option(
    '--debug/--no-debug',
    default=False,
    help="Prints debug data"
)
def snapshot(debug):
    crypto_report = bot.crypto.get_report(debug)
    crypto_reports = bot.crypto.save_report(crypto_report, bot.crypto.get_previous_reports())
    print('Snapshot saved')


@cli.command(
    'output',
    short_help = 'Output the previously stored data',
    help = "Output the previously stored data with 'snapshot'"
)
@click.option(
    '--quiet/--no-quiet',
    default=False,
    help="Set to true if you don't want to print in the console or display an image"
)
@click.option(
    '-r', '--relative/--no-relative',
    default = False,
    help = "If the graph should be plotted relative to its initial value"
)
@click.option(
    '-s', '--symbol',
    default=conf.CURRENCY,
    help="""The currency the graph will be plotted on.
To plot several symbols on the same graph, separate them by a coma.
If plotting several symbols, the --relative option is enabled.
To plot all symbols, use '*'.
Default : FIAT"""
)
@click.option(
    '-d', '--days',
    default=7,
    help="""The number of days over which the graph will be plotted.
If set to 0, the graph will plot all the records.
Default : 7 days"""
)
def output(quiet, relative, symbol, days):
    if symbol == '*':
        symbol = conf.COINS
    else:
        symbol = symbol.split(',')
        for s in symbol:
            assert s in conf.COINS+[conf.CURRENCY]
    if len(symbol) > 1:
        relative = True
    reports = bot.crypto.get_previous_reports()
    if len(reports) == 0:
        msg = "No snapshot in database. Run at least once main.py --snapshot"
        figname = None
    else:
        msg = "*** \n### Crypto report 📈 : \n***\n\n"
        msg += bot.crypto.format_report(reports[-1])
        figname = bot.crypto.plot_symbol(reports, symbol, relative, days)

    bot.io.output(msg, figname, quiet)


if __name__ == "__main__":
    cli()
