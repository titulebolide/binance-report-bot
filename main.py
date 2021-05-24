import bot
import conf
import click

@click.command()
@click.option('--send/--no-send', default=False)
@click.option('--plot-symbol', default='none')
def main(send, plot_symbol):
    crypto_report = bot.crypto.get_report()

    crypto_reports = bot.crypto.save_report(crypto_report, bot.crypto.get_previous_reports())
    figname_value = bot.crypto.plot_symbol(crypto_reports, conf.CURRENCY)
    if plot_symbol != 'none':
        figname_symbol = bot.crypto.plot_symbol(crypto_reports, plot_symbol)

    msg = "*** \n### Compte rendu cryptos 📈 : \n***\n\n"
    msg += bot.crypto.format_report(crypto_report)

    if send:
        bot.io.send_report(msg)
        bot.io.send_img(figname_value)
        if plot_symbol != 'none':
            bot.io.send_img(figname_symbol)

if __name__ == "__main__":
    main()
