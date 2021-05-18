import bot
import click

@click.command()
@click.option('--send/--no-send', default=False)
def main(send):
    st = bot.utils.SymbolTicker()
    crypto_report = bot.crypto.get_report(st)
    miner_report = bot.miner.get_report(st)

    crypto_reports = bot.crypto.save_report(crypto_report, bot.crypto.get_previous_reports())
    figname = bot.crypto.plot_reports(crypto_reports)

    msg = "*** \n### Compte rendu cryptos 📈 : \n***\n\n"
    msg += bot.crypto.format_report(st,crypto_report)
    msg += bot.miner.format_report(st,miner_report)

    if send:
        bot.utils.send_report(msg)
        bot.utils.send_img(figname)

if __name__ == "__main__":
    main()
