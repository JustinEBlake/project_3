# Import dependencies
import pandas as pd
import sqlite3
import yfinance as yf
import requests
import finnhub
import datetime as dt

#Assign companies to variable
company_tickers = ["TSLA", "AAPL", "MCD", "HD", "GOOG", "MSFT", "AXON", "DIS", "BA","EADSY"]



# ------------------------------------------Extract data using yahoo finance library-------------------------

# Get financial statments
def extract_financials(company_tickers=list):

    # Empty list to add company data
    financial_statements = []

    # Append Company data 
    for company_ticker in company_tickers:
        company_data = yf.Ticker(company_ticker)
        financial_statements.append(company_data.financials)

    return financial_statements

    
# Get balance sheets
def extract_bs(company_tickers=list):

    # Empty list to add company data
    balance_sheets = []

    # Append Company data 
    for company_ticker in company_tickers:
        company_data = yf.Ticker(company_ticker)
        balance_sheets.append(company_data.balance_sheet)
    
    return balance_sheets
    
    
# Get stocks
def extract_stocks(company_tickers=list):

    # Empty list to add company data
    stocks = []
    
    # Append Company data 
    for company_ticker in company_tickers:
        company_data = yf.download(company_ticker, period="max")
        stocks.append(company_data)

    return stocks
    

# Get company names
def extract_names(company_tickers=list):
    # Get apikey for finnhub api
    API_KEY = open("api_key.txt", "r").read()

    # Setup Finnhub client
    fh = finnhub.Client(api_key=API_KEY)

    # Dictionary to assign key:value pairs => company_symbol:company_name
    company_names = {
        "company_symbol": [],
        "company_name": []
    }

    # Empty lists to store data in company_names dictionary 
    symbols = []
    names = []

    # Use a for loop to gather all company names then append to empty lists
    for ticker in company_tickers:

        # Get json data
        name = fh.company_profile2(symbol=ticker)["name"]

        # Append data to companies_data dictionary
        symbols.append(ticker)
        names.append(name)
    
    company_names["company_symbol"] = symbols
    company_names["company_name"] = names

    return company_names


#------------------------------------------Transform the data from yahoo finance---------------------------

## TO DO:
# 1) Drop the time from the date columns & And only get years for annual data

# Transform financial statements
def transform_financials(extracted_data, company_tickers=list):
    financial_statements_final = []
    concat_dfs = []

    # index variable to keep track of tickers
    index = 0

    # columns needed
    main_cols = ["Total Revenue", "Gross Profit", "Total Expenses", "Net Income"]

    # Only get columns needed        
    for statement in extracted_data:
    
        # Make a new series with just the required columns
        data = statement.loc[main_cols]

        #Assign to dataframe
        df = pd.DataFrame(data)

        # Transpose data
        df = df.transpose()
        df["company_symbol"] = company_tickers[index]

        # Add 1 to index
        index += 1

        # Rename columns
        df.columns = [["total_revenue", "gross_profit", "total_expenses", "net_income", "company_symbol"]]

        # Reset Index and create date column for old index
        df = df.reset_index(names="date")

        # Final dataframe
        final_df = df[["company_symbol", "date", "total_revenue", "gross_profit", "total_expenses", "net_income"]]

        # Append Dataframe to final_statements_final
        financial_statements_final.append(final_df)

        # Concat all dataframes into single df
        merged_df = pd.concat(financial_statements_final, axis=0, ignore_index=True)

        # Remove (,) from all column names
        merged_df.columns = ["company_symbol", "date", "total_revenue", "gross_profit", "total_expenses", "net_income"]

        

    return merged_df

# Transform Balance Sheets
def transform_bs(extracted_data, company_tickers=list):
    # Empty list to store balance sheets of all companies
    balance_sheets_final = []

    # Columns needed
    main_cols = ["Total Debt", "Share Issued"]

    # index variable for company tickers index
    index = 0

    # Only get columns needed        
    for sheet in extracted_data:
    
        # Make a new series with just the required columns
        data = sheet.loc[main_cols]

        #Assign to dataframe
        df = pd.DataFrame(data)

        # Transpose data
        df = df.transpose()
        df["company_symbol"] = company_tickers[index]

        # Add 1 to index
        index += 1

        # Rename columns
        df.columns = [["total_debt", "shares_issued", "company_symbol"]]

        # Reset Index and create date column for old index
        df = df.reset_index(names="date")

        # Final dataframe
        final_df = df[["company_symbol", "date", "total_debt", "shares_issued"]]

        # Append Dataframe to final_statements_final
        balance_sheets_final.append(final_df)

        # Concat all dataframes into single df
        merged_df = pd.concat(balance_sheets_final, axis=0, ignore_index=True)

        # Remove (,) from column names
        merged_df.columns = ["company_symbol", "date", "total_debt", "shares_issued"]

    return merged_df

# Transform Stocks
def transform_stock(extracted_data, company_tickers=list):
    #Empty list to store all final stock data
    stocks_final = []

    # index variable to keep track of tickers
    index = 0

    # Columns needed
    main_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]

    # Only get columns needed        
    for stock in extracted_data:
    
        # Make a new series with just the required columns
        data = stock[['Open', 'High', 'Low', 'Close', 'Volume']]

        #Assign to dataframe
        df = pd.DataFrame(data)

        # Add company symbol
        df["company_symbol"] = company_tickers[index]

        # Add 1 to index
        index += 1

        # Rename columns
        df.columns = [["open", "high", "low", "close", "volume", "company_symbol"]]

        # Reset Index and create date column for old index
        df = df.reset_index(names="date")

        # Final dataframe
        final_df = df[["company_symbol", "date", "open", "high", "low", "close", "volume"]]

        # Round float numbers
        final_df[["open", "high", "low", "close"]] = final_df[["open", "high", "low", "close"]].round(2)

        # Append Dataframe to final_statements_final
        stocks_final.append(final_df)

        # Concat all dataframes into single df
        merged_df = pd.concat(stocks_final, axis=0, ignore_index=True)

        # Remove (,) from column names
        merged_df.columns = ["company_symbol", "date", "open", "high", "low", "close", "volume"]

    return merged_df

# Transform Company names
def transform_names(extracted_data):
    df = pd.DataFrame(extracted_data)

    return df

#----------------------------------------Load the transformed data into a sqlite database------------------
def load_all_data(company_names,financials, balance_sheets, stocks):

    # load the data to the database
    conn = sqlite3.connect('company_data.sqlite')
    company_names.to_sql('Companies', conn, index=False, if_exists="replace", dtype= {"company_symbol": "VARCHAR PRIMARY KEY"})
    financials.to_sql("Financial_Statements", conn, index=False, if_exists="replace", dtype={"company_symbol": "VARCHAR","date": "DATE", "total_revenue": "INTEGER", "gross_profit": "INTEGER", "total_expenses": "INTEGER", "net_income": "INTEGER", "FOREIGN KEY (company_symbol)": "REFERENCES Companies(company_symbol)" })
    balance_sheets.to_sql("Balance_Sheets", conn, index=False, if_exists="replace", dtype={"company_symbol": "VARCHAR", "date": "DATE", "total_debt": "REAL", "shares_issued": "REAL", "FOREIGN KEY (company_symbol)": "REFERENCES Companies(company_symbol)"})
    stocks.to_sql("Stocks", conn, index=False, if_exists="replace", dtype={"company_symbol": "VARCHAR", "date": "DATE", "open": "REAL", "high": "REAL", "low": "REAL", "close": "REAL", "volume": "INTEGER", "FOREIGN KEY (company_symbol)": "REFERENCES Companies(company_symbol)"})

    conn.commit()
    conn.close()


#----------------------------------------------------------------------------------------------------------
    
# Extract & Transform data
financials = (transform_financials(extract_financials(company_tickers), company_tickers))
balance_sheets = (transform_bs(extract_bs(company_tickers), company_tickers))
stocks = (transform_stock(extract_stocks(company_tickers), company_tickers))
company_tickers = (transform_names(extract_names(company_tickers)))

# Load data into the sqlite db
load_all_data(company_tickers, financials, balance_sheets, stocks)