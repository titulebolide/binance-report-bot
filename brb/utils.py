def check_configuration(conf):
    assert conf.BINANCE_API_KEY != ""
    assert conf.BINANCE_API_SECRET != ""
    if conf.CURRENCY not in ("EUR", "USD"):
        assert conf.OER_APP_ID != ""
