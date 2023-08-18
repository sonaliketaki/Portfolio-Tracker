import streamlit as st
from portfolio_functions import fetch_stock_data, add_stock_to_portfolio, get_portfolio, remove_stock_from_portfolio, fetch_historical_data
from database import connect_to_database
import pandas as pd
import plotly.express as px

try:
    # Connect to the database
    connection = connect_to_database()
    cur = connection.cursor()

    st.title("Manrico's Stock Portfolio")

    st.subheader("Portfolio")
    portfolio = get_portfolio(connection)
  
    if not portfolio:
        st.write("No stocks in portfolio.")
    else:
        portfolio_df = pd.DataFrame(portfolio, columns=["ID", "Symbol", "Last Trade Price", "Shares Owned", "Market Value"])
        portfolio_df[["Last Trade Price"]] = portfolio_df["Last Trade Price"].apply(lambda x: f"${x:.2f}")
        portfolio_df["Market Value"] = portfolio_df["Market Value"].apply(lambda x: f"${x:.2f}")
        st.dataframe(portfolio_df)

    st.subheader("Search for Stock Quote")

    stock_symbol = st.text_input("Enter Stock Symbol (e.g., AAPL):")
    st.write('Select a data range to see', stock_symbol, 'trends')
    start_date = st.date_input('Start Date')
    end_date = st.date_input('End Date')
   
    stock_data = fetch_stock_data(stock_symbol)
    if st.button("Stock Information"):
        historical_data = fetch_historical_data(stock_symbol, start_date, end_date)

        if not historical_data.empty:
            fig = px.line(historical_data, x=historical_data.index, y='close', title=f'{stock_symbol} Stock Trend')
            st.plotly_chart(fig)
        else:
            st.write("No historical data available for the selected dates.")

        if stock_data:
            st.write("Symbol:", stock_data["symbol"])
            st.write("Last Trade Price:", stock_data["last_trade_price"])
            st.write("Open:", stock_data["open"])
            st.write("High:", stock_data["high"])
            st.write("Low:", stock_data["low"])
            st.write("Volume:", stock_data["volume"])
            st.write("Latest trading day:", stock_data["latest_trading_day"])
            st.write("Previous close:", stock_data["previous_close"])
            st.write("Change:", stock_data["change"])
            st.write("Change %:", stock_data["change_percent"])
            
    st.subheader("Add Stock to Portfolio")
    shares_owned = st.number_input("Enter Shares Owned:", min_value=0, step=1, value=0)
    if st.button("Add to Portfolio"):       
        if stock_data:
            if len(portfolio) < 5:
                add_stock_to_portfolio(connection, stock_data["symbol"], stock_data["last_trade_price"], shares_owned)
                st.write("Stock added to Stocks table:", stock_data["symbol"])
        else:
            st.write("Portfolio is already full. Maximum of 5 stocks allowed.")
    else:
        st.write("Invalid stock symbol or data not available.")


    st.subheader("Remove Stock from Portfolio")
    selected_stock = st.selectbox("Select Stock to Remove:", portfolio_df["Symbol"])
    st.subheader("Remove Stock from Portfolio")
    if st.button("Remove Selected Stock"):
        remove_stock_from_portfolio(connection, selected_stock)
        st.write(selected_stock, " successfully removed")

except Exception as error:
    print(error)

finally:
    if cur is not None:
        cur.close()
    if connection is not None:
        connection.close()

