import requests
import pandas as pd
import dateutil.parser
import datetime as dt 
import time
import numpy as np
from ExchangeRates import getExchangeRate

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

    cols = ['token_id', 'price', 'size', 'pair', 'trade_id', 'side', 'source', 'time']
    URL = 'https://api.pro.coinbase.com/products/' + product_id + '/trades'
    pair = product_id.split('-')

    #Making a request
    r = requests.get(url = URL)
    data = r.json()

    #Return dataframe if the request is successful
    if(r.status_code==200):
        #Type casting size and price to float
        df = pd.DataFrame(data).astype({"size": np.float64, "price": np.float64, "trade_id": np.int64})
        
        #Converting time to epoch timestamp
        def toEpoch(row):
            ts = row['time'].split('Z')[0] + ':-0000'
            ts = dt.datetime.strptime(ts, r"%Y-%m-%dT%H:%M:%S.%f:%z").timestamp()
            return ts
        df['time'] = df.apply(toEpoch, axis=1)

        #Setting pair, source and token_id
        df['pair'] = product_id
        df['token_id'] = token_id
        df['source'] = source

        #Converting quoted currency to USD
        df['price'] = df['price'] * getExchangeRate(pair[1], convert_curr)
        return df[cols]
    #Handling case when an empty is acquired
    elif(len(data) == 0):
        print("No records to be shown!")
    else:
        error_message = str(r.status_code) + " " + data['message']
        return "ERROR: " + error_message


if(__name__ == '__main__'):
    print(getTrades('BTC-USD', 'Bitcoin', 'Coinbase'))