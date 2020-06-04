import requests
import pandas as pd
import dateutil.parser
import datetime as dt 
import time
import numpy as np

def getTrades(product_id, token_id, source, convert_curr = 'USD'):
    """
        Parameters:
            product_id (string): Consists of crypto-currency and fiat currency tickers ex: BTC-USD
            token_id (string): Type of cryto-currency
            source (string): Source API
        Returns:
            dataframe: The trades dataframe related to product_id at that time or an error message
            or
            string: if an error occurs
    """

    cols = ['rate', 'amount', 'tradeID', 'type', 'date']
    URL = f"https://poloniex.com/public?command=returnTradeHistory&currencyPair={product_id}"

    #Making a request
    r = requests.get(url = URL)

    #Return dataframe if the request is successful
    if(r.status_code==200):
        #Getting data
        data = r.json()

        #Type casting size and price to float
        df = pd.DataFrame(data)[cols]
        
        #Converting time to epoch timestamp
        def toEpoch(row):
            ts = dt.datetime.strptime(row['date'], r"%Y-%m-%d %H:%M:%S").timestamp()
            return ts
        df['date'] = df.apply(toEpoch, axis=1)

        #Setting pair, source and token_id
        df['pair'] = product_id
        df['token_id'] = token_id
        df['source'] = source
        df.columns = ['Trade_Price', 'Trade_Size', 'Trade_ID', 'Side', 'Tstamp'] + ['Pair', 'Token_ID', 'Source']
        return df[['Token_ID', 'Trade_Price', 'Trade_Size', 'Pair', 'Trade_ID', 'Side', 'Source', 'Tstamp']]
    else:
        return "ERROR: " + str(r.status_code)

if(__name__ == '__main__'):
    print(getTrades('BTC_ETH', 'BTC', 'Poleniex'))