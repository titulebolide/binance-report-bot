# Crypto Bot
Not a real cryto bot actually, it just fetch the various APIs to produce a nice markdown report that can be sent with the matrix bot

The intent of this bot is to take a snapshot of your binance wallet, e.g. the current balances and store it for further plotting.

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

## Usage
To save a snapshot of the binance accunt run:
```
python main.py --snapshot
```
To output the previously saved snapshots
```
python main.py --output OUTPUT_TYPE
```
With OUTPUT_TYPE being in:
- `print`
- `http` (can be used with the `--port` option)
