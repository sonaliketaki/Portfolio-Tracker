import psycopg2

def connect_to_database():
    db_params = {
        "dbname": "stock_portfolio",
        "user": "postgres",
        "password": "user123",
        "host": "localhost",
        "port": "5432", 
    }
    connection = psycopg2.connect(**db_params)
    initialize_schema(connection)  
    return connection

def initialize_schema(connection):
    with connection.cursor() as cursor:
        # Create Stocks table if it doesn't exist
        cursor.execute(
           """CREATE TABLE IF NOT EXISTS Stocks (
                stock_id SERIAL PRIMARY KEY,
                symbol VARCHAR(10) UNIQUE,
                last_trade_price DECIMAL(10, 2)
            )"""
        )
        
        # Create Portfolio table if it doesn't exist
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Portfolio (
                id SERIAL PRIMARY KEY,
                stock_id SERIAL REFERENCES Stocks(stock_id),
                shares_owned INTEGER,
                market_value  INTEGER
            )"""
        )
    connection.commit()
