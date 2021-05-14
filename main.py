import requests
import numpy as np
import conf
import gspread
from oauth2client.service_account import ServiceAccountCredentials

sheet = gspread.service_account(
    filename=conf.GOOGLE_TOKEN_FILE
).open_by_key(conf.SHEET_ID).get_worksheet(0)

sheet_data = np.array(sheet.get('1:3'))

cryptos = set(sheet_data[0,2:])

def getSymbolTicker(symbol):
    data = requests.get(
     'https://min-api.cryptocompare.com/data/price?fsym='+symbol+'&tsyms=EUR&api_key='+conf.CRYPTOCOMPARE_API_KEY
    )
    return data.json()['EUR']

symbol_ticker = {}
symbol_eur_value = {}
for col in range(2, sheet_data.shape[1]):
    symbol = sheet_data[0,col]
    quantity = float(sheet_data[2,col])
    if symbol in symbol_ticker:
        ticker = symbol_ticker[symbol]
    else:
        ticker = getSymbolTicker(symbol)
        symbol_ticker[symbol] = ticker
    if symbol in symbol_eur_value:
        symbol_eur_value[symbol] += ticker*quantity
    else:
        symbol_eur_value[symbol] = ticker*quantity


msg = "Compte rendu cryptos:\n"
for symbol, value in symbol_eur_value.items():
    msg += "- *{}* : {} €\n".format(symbol, value)
msg+="\n*Total* : {}€".format(sum(symbol_eur_value.values()))

requests.post("http://127.0.0.1:"+str(conf.BOT_PORT), data={"msg":msg})
