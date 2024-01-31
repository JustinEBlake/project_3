import pandas as pd
import sqlite3

def extract():
    user_input = input("Enter csv to filter (e.g. 'apple_balance', 'company_list', 'home_depot_balance', 'mcdonalds_balance', 'tesla_balance')")
    # use apis or anything else here as needed
    if user_input == 'apple_balance':
        return pd.read_csv('Resources/aapl_bal.csv')
    
    elif user_input == 'company_list':
        return pd.read_csv('Resources/company.csv')
    
    elif user_input == 'home_depot_balance':
        return pd.read_csv('Resources/hd_bal.csv')
    
    elif user_input == 'mcdonalds_balance':
        return pd.read_csv('Resources/mcd_bal.csv')
    
    elif user_input == 'tesla_balance':
        return pd.read_csv('Resources/tsla_bal.csv')
    
    else:
        return print('Invalid input.')

def transform(data):
    # perform data transformations and return tables
    share_issued = data[['Share Issued', 'Date']].groupby(['Share Issued', 'Date']).size().reset_index(drop=False).reset_index(drop=False, names='id')
    total_debt = data[['Total Debt', 'Date']].groupby(['Total Debt', 'Date']).size().reset_index(drop=False).reset_index(drop=False, names='id')

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

