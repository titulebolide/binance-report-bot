import bot

st = bot.utils.SymbolTicker()
crypto_report = bot.crypto.get_report(st)
miner_report = bot.miner.get_report(st)

msg = "*** \n### Compte rendu cryptos 📈 : \n***\n\n"
msg += bot.crypto.format_report(st,crypto_report)
msg += bot.miner.format_report(st,miner_report)

bot.utils.send_report(msg)
