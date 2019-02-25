from dotenv import load_dotenv
import json
import os
import requests
import datetime as dt
import csv

#converting float to USD adapted from https://stackoverflow.com/questions/21208376/converting-float-to-dollars-and-cents
def as_currency(amount):
        return '${:,.2f}'.format(amount)

load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

# see: https://www.alphavantage.co/support/#api-key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
# print("API KEY: " + api_key) # TODO: remove or comment-out this line after you have verified the environment variable is getting read properly

# Modifying my previous data validation to work for this project
while True:
  datatype_pass = True
  symbol_length_pass = True
  program_pass = True
  stock_symbol = input("Please enter the stock symbol you would like to hear advice for...")

  #Input validation
  if not stock_symbol.isalpha():
    print("INPUT DATA TYPE ERROR! Please only enter one to five characters! Let's try again.")
    datatype_pass = False
  if datatype_pass == True:
    # New York Stock Exchange (NYSE) and American Stock Exchange (AMEX) listed stocks have three characters or less. 
    # Nasdaq-listed securities have four or five characters.
    if int(len(stock_symbol)) not in range(1,5):
        print("Please ensure the length of the symbol is between three and five. Let's try again.")
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

  request_url = ('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+stock_symbol+'&apikey='+api_key)
  response = requests.get(request_url)
  print(type(response.status_code))

  parsed_response = json.loads(response.text)

  last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
  Time_Series = parsed_response["Time Series (Daily)"]
  dates = list(Time_Series.keys())
  latest_day = dates[0]
  latest_close = parsed_response["Time Series (Daily)"][latest_day]["4. close"]


  high_prices = []
  low_prices = []

  for date in dates:
    high_price = Time_Series[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = Time_Series[date]["3. low"]
    low_prices.append(float(low_price))

    recent_high = max(high_prices)
    recent_low = min(low_prices)

  # TODO: write response data to a CSV file

  csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "price.csv")
  csv_headers = ["timestamp","open","high","low","close","volume"]


  with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
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
  
  print(f"WRITING DATA TO CSV: {csv_file_path}")

  # TODO: further revise the example outputs below to reflect real information
  print("-------------------------")
  print(f"SELECTED SYMBOL: {stock_symbol}")
  print("-------------------------")
  print("REQUESTING STOCK MARKET DATA")
  print("REQUEST AT: 2018-02-20 14:00") # TODO: dynamic datetime
  print("-------------------------")
  print(f"LAST REFRESH: {last_refreshed}")
  print(f"LATEST CLOSE: {as_currency(float(latest_close))}")
  print(f"RECENT HIGH: {as_currency(float(recent_high))}")
  print(f"RECENT LOW: {as_currency(float(recent_low))}")
  print("-------------------------")
  print("RECOMMENDATION: BUY!") # TODO
  print("BECAUSE: TODO") # TODO
  print("-------------------------")

  print("-------------------------")
  print("HAPPY INVESTING!")
  print("-------------------------")