# Portfolio-Tracker
This is a Streamlit-based web application for managing a stock portfolio. The app allows users to view their portfolio, search for stock quotes, add and remove stocks from the portfolio, and view historical stock trends.


<img width="887" alt="image" src="https://github.com/sonaliketaki/Portfolio-Tracker/assets/83692145/074586b0-9844-4a24-a5bd-ac3553ca2305">


## Installation

1. Make sure you have Python installed (version 3.7 or higher).
2. Clone this repository to your local machine.
   ```python
   git clone https://github.com/sonaliketaki/Portfolio-Tracker.git
   ```
3. Navigate to the project directory and create a virtual environment (recommended)
  ```python
  python -m venv venv
  ```
  and activate the environment.
  
  On Linux, OsX or in a Windows Git Bash terminal it's
  
  ```bash
  source .venv/Scripts/activate
  ```
  
  or alternatively
  
  ```bash
  source .venv/bin/activate
  ```
  
  In a Windows terminal it's
  
  ```bash
  .venv/Scripts/activate.bat
  ```
4. Install the required packages using the following command:

  ```bash
  pip install -r requirements.txt
  ```

5. Set up the PostgreSQL database:
  Make sure you have PostgreSQL installed and running.
  Update the database configuration details in db_params located in the database.py file according to your setup.

  ```python
  db_params = {
          "dbname": "stock_portfolio",
          "user": "owner",
          "password": "password",
          "host": "localhost",
          "port": "5432", 
      }
  ```
    
  Run the following commands to create the required tables:
  
  ```bash
  python database.py
  ```

## Usage
Run the application using the following command:
```bash
streamlit run main.py
```
The application will open in your default web browser.

## Features
1. View Portfolio: Displays the stocks you own along with their market values.
2. Search for Stock Quote: Enter a stock symbol and choose a date range to see trends.
3. Add Stock to Portfolio: Add a new stock to your portfolio.
4. Remove Stock from Portfolio: Remove a stock from your portfolio.

## Acknowledgments
The application uses the Alpha Vantage API to fetch stock data.
The database is managed using PostgreSQL.
