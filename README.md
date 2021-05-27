# Crypto Bot
Not a real cryto bot actually, it just fetch the various APIs to produce a nice markdown report that can be sent with the matrix bot

The intent of this bot is to take a snapshot of your binance wallet, e.g. the current balances and store it for further plotting.

## Install

Create the file `conf.py` based on `conf.template.py`.

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
- `print` (simply display the report)
- `http` (can be used with the `--port` option) (send the report to an http server, useful to transmit the data to another bot)

The generated graph can be plotted against another currency than the FIAT, e.g. for EOS (EOS will have to be in the COINS list in the conf file):
```
python main.py --output print --plot-symbol EOS
```
