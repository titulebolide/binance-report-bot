from conf_default import *
try:
    from conf_user import *
except ModuleNotFoundError:
    try:
        from conf import *
        print("WARNING : please rename conf.py to conf_user.py")
    except ModuleNotFoundError:
        raise ModuleNotFoundError("File conf_user.py missing. Please check the installation section in the README.")

#Conf check
assert BINANCE_API_KEY != ""
assert BINANCE_API_SECRET != ""
if CURRENCY not in ("EUR", "USD"):
    assert OER_APP_ID != ""
