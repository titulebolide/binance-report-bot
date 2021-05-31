# Binance Report Bot
The intent of this bot is to take a snapshot of your binance wallet, e.g. the current balances and store it for further plotting.

## Install

Create the file `conf.py` based on `conf.template.py`.

Then run
```
pip install -r requirements.txt
```

## Usage
To save a snapshot of the binance account run:
```bash
python main.py snapshot
```
To show the previously saved snapshots
```bash
python main.py output # --help for options
```

### Deployment
One can use crontab to use this code:
```cron
0 * * * * cd [FOLDER] ; python3 main.py snapshot
2 19 * * * cd [FOLDER] ; python3 main.py output [OPTIONS]
```
To have a snaphsot made every hour and a report made every day at 19:02.

## Output example
Plot `EOS` holdings:
```bash
python3 main.py output --symbol EOS
```

Plot `ICX` relative holdings:
```bash
python3 main.py output --symbol ICX --relative
```

Plot `ICX` and `EOS` holdings:
```bash
python3 main.py output --symbol ICX,EOS
```

Plot the holdings of all soins registered in the conf file:
```bash
python3 main.py output --symbol * # or '*' if using zsh
```
