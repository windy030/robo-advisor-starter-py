import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
from dotenv import load_dotenv
import json
import os
import requests
import datetime as dt
import csv

dashline = "-------------------------"

def to_usd(amount):
        return '${:,.2f}'.format(amount)

def compile_URL(stock_symbol):
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + str(stock_symbol)
        return url

def get_response(stock_symbol):
    API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    return parsed_response


if __name__ == "__main__":
  now = dt.datetime.now()
  load_dotenv() 
  api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

  while True:
    datatype_pass = True
    symbol_length_pass = True
    program_pass = True
    stock_symbol = input("Please enter the stock symbol you would like to hear advice for...")

    #Input validation
    if not stock_symbol.isalpha():
      print("INPUT DATA TYPE ERROR! Please only enter characters! Let's try again.")
      datatype_pass = False
    if datatype_pass == True:
      # New York Stock Exchange (NYSE) and American Stock Exchange (AMEX) listed stocks have three characters or less. 
      # Nasdaq-listed securities have four or five characters.
      if int(len(stock_symbol)) not in range(1,6):
          print("INPUT LENGTH ERROR! Please ensure the length of the symbol is between one and five characters. Let's try again.")
          symbol_length_pass = False
      if symbol_length_pass ==True:    
          #validation adapted from https://github.com/hiepnguyen034/robo-stock/blob/master/robo_advisor.py
          data=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stock_symbol+'&apikey='+api_key)
          if 'Error' in data.text:
              print("Sorry.The stock symbol is either incorrect or cannot be found online. The program will terminate now...")
              break
          else:
              program_pass = True
              break

  if program_pass == True:

    # making a request after successful data validation
    request_url = ('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stock_symbol+'&apikey='+api_key)
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)

    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    Time_Series = parsed_response["Time Series (Daily)"]
    dates = list(Time_Series.keys())
    latest_day = dates[0]
    latest_close = parsed_response["Time Series (Daily)"][latest_day]["4. close"]

    high_prices = []
    low_prices = []
    close_prices = []

    for date in dates:
      high_price = Time_Series[date]["2. high"]
      high_prices.append(float(high_price))

      low_price = Time_Series[date]["3. low"]
      low_prices.append(float(low_price))

      close_price = Time_Series[date]["4. close"]
      close_prices.append(float(close_price))

    recent_high = max(high_prices)
    recent_low = min(low_prices)

    # write response data to a CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "price.csv")
    csv_headers = ["timestamp","open","high","low","close","volume"]

    with open(csv_file_path, "w") as csv_file: 
      writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
      writer.writeheader() 
      for date in dates:
        daily_price = Time_Series[date]
        writer.writerow({
          "timestamp": date, 
          "open": daily_price["1. open"], 
          "high": daily_price["2. high"],
          "low" : daily_price["3. low"],
          "close": daily_price["4. close"],
          "volume": daily_price["5. volume"]
          })
    
    # get the average high prices and compare it to the latest closing price
    average_high = np.mean(high_prices)
    if float(latest_close) >= average_high:
      decision = "DON'T BUY!"
      explanation = "the stock is overvalued - the latest closing price is equal to or higher than the average high price for the past four months."
    else:
      decision = "BUY!"
      explanation = "the stock is undervalued - the latest closing price is lower than the average high price for the past four months."

    print(f"WRITING DATA TO CSV: {csv_file_path}")
    print(dashline)
    print(f"SELECTED SYMBOL: {stock_symbol}")
    print(dashline)
    print("REQUESTING STOCK MARKET DATA")
    print("REQUEST AT: " + str(now.strftime("%Y-%m-%d %H:%M:%S"))) 
    print("-------------------------")
    print(f"LAST REFRESH: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW: {to_usd(float(recent_low))}")
    print(dashline)
    print("RECOMMENDATION: " + decision) 
    print("BECAUSE: " + explanation) 
    print(dashline)
    print(dashline)
    print("HAPPY INVESTING!")
    print(dashline)

    # Challenge 3: Plotting Prices over Time / data visualization
    dates.reverse()
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(dates,close_prices)
    ax.xaxis.set_major_locator(MaxNLocator(4))
    plt.ylabel("Prices")
    plt.xlabel("Dates")
    formatter = ticker.FormatStrFormatter('$%1.2f')
    ax.yaxis.set_major_formatter(formatter)
    ax.set_ylim([recent_low,recent_high])
    plt.title("Stock Prices Over the Past Four Months")
    plt.tight_layout()
    plt.show()