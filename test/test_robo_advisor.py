from app.robo_advisor import to_usd, compile_URL

def test_to_usd():
    assert to_usd(3.1415926) == "$3.14"


def test_compile_URL():
    stock = "AMZN"
    assert compile_URL(stock) == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN"