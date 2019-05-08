from app.robo_advisor import to_usd

def test_to_usd():
    assert to_usd(3.1415926) == "$3.14"