# Your binance API keys
# ATTENTION : CENSOR THESE KEYS IF ASKED TO PASTE THIS FILE
BINANCE_API_KEY = ""
BINANCE_API_SECRET = ""

# The list of coins that you would like to follow
COINS = ["BTC","ADA","ATOM","BAT","BTT","CAKE","DASH","EOS","ETC","ICX","IOTA","NEO","OMG","ONT","QTUM","ROSE","TRX","VET","WIN","XLM"]

# The currency with which the reports will be printed
CURRENCY = "EUR" #Or USD

# The symbol of your currency
CURRENCY_SYMBOL = "€"

# Set here the different diffs you want to see in the text report
# E.g. if you want tp see the yearly, monthly, weekly or daily diffs
DIFFS_POSITIONS = [
    {"ts_delta" : 60*60*24, "text" : "day"},
    {"ts_delta" : 60*60*24*7, "text" : "week"},
    {"ts_delta" : 60*60*24*30, "text" : "month"},
    #{"ts_delta" : 60*60*24*365, "text" : "year"},
]

# Set this to false if your terminal does not support rich printing
RICH_PRINTING = True

# Leave empty if you don't want to use apprise notifications.
# Use an apprise service that supports attachment (e.g. Discord, Telegram or Emails)
# Examples:
#   APPRISE_URLS = ["discord://something"] if you want to use only discord
#   APPRISE_URLS = ["discord://something", "telegram://something"] if you want to use both telegram and discord, don't miss the comma ","
APPRISE_URLS = []

# openexchangerates.org api key. Mandatory if CURRENCY is not EUR or USD
# Get yours here : https://openexchangerates.org/signup/free
OER_APP_ID = ""
