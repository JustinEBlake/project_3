import pandas as pd
import sqlite3

def extract():
    #obtaining user input
    user_input = input("Enter csv to filter (e.g. 'companies', 'AAPL_balance', 'HD_balance', 'MCD_balance', 'TSLA_balance')")
    #parsing through user inputap
    if user_input == 'AAPL_balance':
        return pd.read_csv('Resources/aapl_bal.csv')
    
    elif user_input == 'HD_balance':
        return pd.read_csv('Resources/hd_bal.csv')
    
    elif user_input == 'MCD_balance':
        return pd.read_csv('Resources/mcd_bal.csv')
    
    elif user_input == 'TSLA_balance':
        return pd.read_csv('Resources/tsla_bal.csv')
    
    elif user_input == 'companies':
        return pd.read_csv('Resources/company.csv')
    
    else:
        return print('Invalid input.')

def transform(data):
    #transform the data
    share_issued = data[['company_name', 'Date', 'Share Issued']].groupby(['company_name', 'Date', 'Share Issued']).size().reset_index(drop=False).reset_index(drop=False, names='id')
    total_debt = data[['company_name', 'Date', 'Total Debt']].groupby(['company_name', 'Date', 'Total Debt']).size().reset_index(drop=False).reset_index(drop=False, names='id')


    return share_issued, total_debt


def load(share_issued, total_debt):
    # load the data to the database
    conn = sqlite3.connect('stocks.sqlite')
    share_issued.to_sql('share_issued', conn, index=False, if_exists='replace', dtype={'id': 'INTEGER PRIMARY KEY'})
    total_debt.to_sql('total_debt', conn, index=False, if_exists='replace', dtype={'id': 'INTEGER PRIMARY KEY'})
    conn.close()

def read(table_name):
    # query the desired column
    df = pd.read_sql_table(table_name, "sqlite:///stocks.sqlite", index_col='id')

    return df


if __name__ == '__main__':
    extract_data = extract()
    s_i, t_d = transform(extract_data)
    load(s_i, t_d)
    print(read('share_issued'))
    print(read('total_debt'))

