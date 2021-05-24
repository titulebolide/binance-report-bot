import bot
import click

@click.command()
@click.option('--send/--no-send', default=False)
def main(send):
    crypto_report = bot.crypto.get_report()

    crypto_reports = bot.crypto.save_report(crypto_report, bot.crypto.get_previous_reports())
    figname = bot.crypto.plot_reports(crypto_reports)

    msg = "*** \n### Compte rendu cryptos 📈 : \n***\n\n"
    msg += bot.crypto.format_report(crypto_report)

    if send:
        bot.io.send_report(msg)
        bot.io.send_img(figname)

if __name__ == "__main__":
    main()
