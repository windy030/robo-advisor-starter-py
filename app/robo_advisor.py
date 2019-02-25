from dotenv import load_dotenv
import json
import os
import requests

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
            print('The stock you are looking for is not here')
            break
        else:
            program_pass = True
            break

print(program_pass)
symbol = "NFLX" # TODO: capture user input, like... input("Please specify a stock symbol: ")

# see: https://www.alphavantage.co/documentation/#daily (or a different endpoint, as desired)
# TODO: assemble the request url to get daily data for the given stock symbol...

# TODO: use the "requests" package to issue a "GET" request to the specified url, and store the JSON response in a variable...

# TODO: further parse the JSON response...

# TODO: traverse the nested response data structure to find the latest closing price and other values of interest...
latest_price_usd = "$100,000.00"

#
# INFO OUTPUTS
#

# TODO: write response data to a CSV file

# TODO: further revise the example outputs below to reflect real information
print("-----------------")
print(f"STOCK SYMBOL: {symbol}")
print("RUN AT: 11:52pm on June 5th, 2018")
print("-----------------")
print("LATEST DAY OF AVAILABLE DATA: June 4th, 2018")
print(f"LATEST DAILY CLOSING PRICE: {latest_price_usd}")
print("RECENT AVERAGE HIGH CLOSING PRICE: $101,000.00")
print("RECENT AVERAGE LOW CLOSING PRICE: $99,000.00")
print("-----------------")
print("RECOMMENDATION: Buy!")
print("RECOMMENDATION REASON: Because the latest closing price is within threshold XYZ etc., etc. and this fits within your risk tolerance etc., etc.")
print("-----------------")
