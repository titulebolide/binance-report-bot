# Crypto Bot
Not a real cryto bot actually, it just fetch the various APIs to produce a nice markdown report that can be sent with the matrix bot

## Install

Create a `conf.py` file at the root of this project with the following infos:
```
BINANCE_API_KEY = ""
BINANCE_API_SECRET = ""
CRYPTOCOMPARE_API_KEY = ""
BOT_PORT = 34546
MINER_ADRESS = ""
```

Then run
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
