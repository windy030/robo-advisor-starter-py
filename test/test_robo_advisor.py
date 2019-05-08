from app.robo_advisor import to_usd, compile_URL, get_response

def test_to_usd():
    assert to_usd(3.1415926) == "$3.14"

def test_compile_URL():
    stock = "AMZN"
    assert compile_URL(stock) == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMZN"

def test_get_response():
    stock_symbol = "AMZN"
    parsed_response = get_response(stock_symbol)
    # adapated from https://github.com/s2t2/robo-advisor-screencast/pull/1/files
    assert isinstance(parsed_response, dict)