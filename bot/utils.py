import binance
import requests
import conf
import os

class SymbolTicker:
    def __init__(self):
        self.symbol_ticker = {}
        datas = binance.Client(conf.BINANCE_API_KEY, conf.BINANCE_API_SECRET).get_symbol_ticker()
        for data in datas:
            if data['symbol'].endswith('EUR'):
                self.symbol_ticker[data['symbol'][-3]] = data['price']

    def getTicker(self, symbol):
        if not symbol in self.symbol_ticker:
            data = requests.get(
                'https://min-api.cryptocompare.com/data/price?fsym='+symbol+'&tsyms=EUR&api_key='+conf.CRYPTOCOMPARE_API_KEY
            ).json()
            if not "EUR" in data:
                print(data, symbol)
                price=0
            else:
                price=data["EUR"]
            self.symbol_ticker[symbol] = price
        return self.symbol_ticker[symbol]

def send_report(msg):
    try:
        requests.post("http://127.0.0.1:"+str(conf.BOT_PORT), data={"txt":msg})
    except requests.exceptions.ConnectionError:
        print(msg)

def send_img(img):
    try:
        requests.post("http://127.0.0.1:"+str(conf.BOT_PORT), data={
            "img": os.path.join(os.getcwd(), img)
        })
    except requests.exceptions.ConnectionError:
        pass
