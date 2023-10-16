from kafka import KafkaProducer
import os, json
from dotenv import load_dotenv
import time
import finnhub

# Define producer
producer = KafkaProducer(bootstrap_servers=['34.101.49.216:9093'],
                         value_serializer = lambda x: json.dumps(x).encode('utf-8'))
                        # why do we need utf-8 encoding? because kafka need byte string, not regular string

# Define finnhub client
load_dotenv(dotenv_path='key/finnhub.env') # Load the .env file
api_key = os.getenv('FINNHUB_API_KEY') # Get the API key
finnhub_client = finnhub.Client(api_key=api_key)

# Define request function
def getStock(symbol):
    stock_quote = {}
    try:
        stock_quote = finnhub_client.quote(symbol)
        stock_quote["symbol"] = symbol
    except Exception as e:
        print(f"Error fetching quote for {symbol}: {e}")
    return stock_quote

# # Documentation here https://github.com/Finnhub-Stock-API/finnhub-python
# The output print(finnhub_client.quote('AMZN')) will be like this
# {'c': 127.96, 'd': 2, 'dp': 1.5878, 'h': 128.4485, 'l': 124.13, 'o': 124.16, 'pc': 125.96, 't': 1696622402}
# current_price, difference, different_precentage, high, low, open_price, previous_close_price, timestamp
# Finnhub API has 60 request limit per minute


stock_symbols = ['NVDA', 'AMZN', 'GOOGL', 'MSFT']
while True:
    for symbol in stock_symbols:
        try:
            stock_dict = getStock(symbol)
            producer.send("stock", value=stock_dict)
            print(f"Sending: {json.dumps(stock_dict, indent=2)}")
        except Exception as e:
            print(f"Producer error: {e}")
    time.sleep(60)
