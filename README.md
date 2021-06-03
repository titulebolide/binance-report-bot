# Binance Report Bot
The intent of this bot is to take a snapshot of your binance wallet, e.g. the current balances and store it for further plotting.

## Install

Create the file `conf.py` based on `conf.template.py`.

Then run
```
pip install -r requirements.txt
```

## Basic Usage
To save a snapshot of the binance account run:
```bash
python main.py snapshot
```
To show the previously saved snapshots
```bash
python main.py output # --help for options
```

## Deployment
One can use crontab to use this code:
```cron
0 * * * * cd [FOLDER] ; python3 main.py snapshot
2 19 * * * cd [FOLDER] ; python3 main.py output [OPTIONS]
```
To have a snaphsot made every hour and a report made every day at 19:02.

The output can be sent to an external service, that can be configured with the APPRISE_URL parameter. See [here](https://github.com/caronc/apprise/wiki) to choose your external service and to create your APPRISE_URL. Please use a service that supports attachment, in order to send images. Recommended services : [Discord](https://github.com/caronc/apprise/wiki/Notify_discord), [Telegram](https://github.com/caronc/apprise/wiki/Notify_telegram) or [Email](https://github.com/caronc/apprise/wiki/Notify_email).

## Output example
Plot `EOS` *equivalent* holdings:
```bash
python3 main.py output --symbol EOS
```

Plot `ICX` relative equivalent holdings:
```bash
python3 main.py output --symbol ICX --relative
```

Plot `ICX` and `EOS` equivalent holdings since three days ago:
```bash
python3 main.py output --symbol ICX,EOS --days 3
```

Plot the equivalent holdings of all soins registered in the conf file:
```bash
python3 main.py output --symbol * # or '*' if using zsh
```

**Note** : The *equivalent holding* is your portfolio's value in a certain currency. It represents what you would be holding if all your portfolio was under this single currency.
