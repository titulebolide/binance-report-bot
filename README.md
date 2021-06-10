# Binance Report Bot

:warning: **0.5.0 -> 0.6.0 INTRODUCES BREAKING CHANGES IN THE API** :warning:
Replace `python3 main.py` calls by `python3 -m brb`

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
python3 -m brb snapshot
```
To show the previously saved snapshots
```bash
python3 -m brb output # --help for options
```

## Deployment
One can use crontab to use this code:
```cron
0 * * * * cd [FOLDER] ; python3 -m brb snapshot
2 19 * * * cd [FOLDER] ; python3 -m brb output --quiet
```
To have a snaphsot made every hour and a report made every day at 19:02.

The output can be sent to an external service, that can be configured with the APPRISE_URL parameter. See [here](https://github.com/caronc/apprise/wiki) to choose your external service and to create your APPRISE_URL. Please use a service that supports attachment, in order to send images. Recommended services : [Discord](https://github.com/caronc/apprise/wiki/Notify_discord), [Telegram](https://github.com/caronc/apprise/wiki/Notify_telegram) or [Email](https://github.com/caronc/apprise/wiki/Notify_email).

## Output example
Plot `EOS` *equivalent* holdings:
```bash
python3 -m brb output --symbol EOS
```

Plot `ICX` relative equivalent holdings:
```bash
python3 -m brb output --symbol ICX --relative
```

Plot `ICX` and `EOS` equivalent holdings since three days ago:
```bash
python3 -m brb output --symbol ICX,EOS --days 3
```

Plot the equivalent holdings of all soins registered in the conf file:
```bash
python3 -m brb output --symbol * # or '*' if using zsh
```

**Note** : The *equivalent holding* is your portfolio's value in a certain currency. It represents what you would be holding if all your portfolio was under this single currency.

## CLI specification
```bash
$ python3 -m brb --help
Usage: python -m brb [OPTIONS] COMMAND [ARGS]...

  Binance Report Bot

  Take a snapshot of your binance wallet, e.g. the current balances and store
  it for further plotting.

Options:
  --debug / --no-debug  Prints debug data
  --help                Show this message and exit.

Commands:
  output    Output the previously stored data
  snapshot  Take a snapshot of your wallet
```

```bash
$ python3 -m brb snapshot --help
Usage: main.py snapshot [OPTIONS]

  Take a snapshot of the binance wallet and save it for further plotting

Options:
  --help                Show this message and exit.
```

```bash
$ python3 -m brb output --help
Usage: main.py output [OPTIONS]

  Output the previously stored data with 'snapshot'

Options:
  --quiet / --no-quiet            Set to true if you don't want to print in
                                  the console or display an image
  -r, --relative / --no-relative  If the graph should be plotted relative to
                                  its initial value
  -s, --symbol TEXT               The currency the graph will be plotted on.
                                  To plot several symbols on the same graph,
                                  separate them by a coma. If plotting several
                                  symbols, the --relative option is enabled.
                                  To plot all symbols, use '*'. Default : FIAT
  -d, --days INTEGER              The number of days over which the graph will
                                  be plotted. If set to 0, the graph will plot
                                  all the records. Default : 7 days
  --help                          Show this message and exit.
```
