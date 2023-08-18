import requests
import psycopg2
from database import connect_to_database
import pandas as pd

def fetch_stock_data(symbol):
    api_key = "PWRN1YWDMX74MVP9"
    # api_key = "R6J9EC3G774J8DQE"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    
    response = requests.get(url)
    data = response.json()

    if "Global Quote" in data:
        stock_data = data["Global Quote"]
        return {
            "symbol": stock_data["01. symbol"],
            "last_trade_price": float(stock_data["05. price"]),
            "open": stock_data["02. open"],
            "high": stock_data["03. high"],
            "low": stock_data["04. low"],
            "volume": stock_data["06. volume"],
            "latest_trading_day": stock_data["07. latest trading day"],
            "previous_close": stock_data["08. previous close"],
            "change": stock_data["09. change"],
            "change_percent": stock_data["10. change percent"],
        }
    
    else:
        return None

def add_stock_to_portfolio(connection, symbol, last_trade_price, shares_owned):
    market_value = last_trade_price * shares_owned
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO Stocks (symbol, last_trade_price) "
            "VALUES (%s, %s) "
            "ON CONFLICT (symbol) DO NOTHING", 
            (symbol, last_trade_price)
        )
        cursor.execute(
            "SELECT stock_id FROM Stocks WHERE symbol = %s",
            (symbol,)
        )
        stock_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO Portfolio (stock_id, shares_owned, market_value) "
            "VALUES (%s, %s, %s)",
            (stock_id, shares_owned, market_value)
        )
    connection.commit()

def get_portfolio(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT p.id, s.symbol, s.last_trade_price, p.shares_owned, p.market_value "
            "FROM Portfolio p, Stocks s " 
            "WHERE p.stock_id = s.stock_id"
        )
        portfolio = cursor.fetchall()
    return portfolio

def remove_stock_from_portfolio(connection, symbol):
    with connection.cursor() as cursor:
        cursor.execute("SELECT stock_id FROM Stocks WHERE symbol = %s", (symbol,))
        stock_id = cursor.fetchone()[0]

        cursor.execute("DELETE FROM Portfolio WHERE stock_id = %s", (stock_id,))
        
    connection.commit()

def fetch_historical_data(symbol, start_date, end_date):
    api_key = "R6J9EC3G774J8DQE"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    response = requests.get(url)
    data = response.json()
    
    if "Time Series (Daily)" in data:
        time_series = data["Time Series (Daily)"]
        historical_data = []
        for date, values in time_series.items():
            date = pd.to_datetime(date)
            close_price = float(values["4. close"])
            historical_data.append({"date": date, "close": close_price})
        historical_df = pd.DataFrame(historical_data)
        historical_df.set_index("date", inplace=True)
        return historical_df
    else:
        return pd.DataFrame() 