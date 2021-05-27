import bot
import conf
import click

@click.command()
@click.option('--snapshot/--no-snapshot', default=False)
@click.option('--output', default='none')
@click.option('--port', default=8080)
@click.option('--plot-symbol', default=conf.CURRENCY)
def main(snapshot, output, port, plot_symbol):
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
