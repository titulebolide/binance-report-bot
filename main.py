import bot
import conf
import click

@click.command()
@click.option(
    '--snapshot/--no-snapshot',
    default=False,
    help = "Take a snapshot of the binance wallet and save it"
)
@click.option(
    '--output',
    default='none',
    help='If used, the script will ouput the previously saved data the way it is asked to'
)
@click.option(
    '--port',
    default=8080,
    help="The port to send the data. To be used with --output http"
)
@click.option(
    '--plot-symbol',
    default=conf.CURRENCY,
    help="The currency the graph will be plotted on. Default : FIAT"
)
def main(snapshot, output, port, plot_symbol):
    """
    Take a snapshot of your binance wallet, e.g. the current balances and store it for further plotting.
    """

    assert plot_symbol in conf.COINS+[conf.CURRENCY]

    if not snapshot and output == 'none':
        print("Nothing to do. Run main.py --help for more details")

    if snapshot:
        crypto_report = bot.crypto.get_report()
        crypto_reports = bot.crypto.save_report(crypto_report, bot.crypto.get_previous_reports())
        print('Snapshot saved')

    if output != 'none':
        reports = bot.crypto.get_previous_reports()
        if len(reports) == 0 :
            msg = "No snapshot in database. Run at least once main.py --snapshot"
            figname = None
        else:
            msg = "*** \n### Crypto report 📈 : \n***\n\n"
            msg += bot.crypto.format_report(reports[-1])
            figname = bot.crypto.plot_symbol(reports, plot_symbol)

        bot.io.output(msg, figname, output, port)

if __name__ == "__main__":
    main()
