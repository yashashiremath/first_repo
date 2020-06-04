import requests
import pandas as pd
import dateutil.parser
import datetime as dt 
import time
import numpy as np
from ExchangeRates import getExchangeRate

def coinbasePreprocess(dataframe):
    #Converting time to epoch timestamp
    def toEpoch(row):
        ts = row['time'].split('Z')[0] + ':-0000'
        ts = dt.datetime.strptime(ts, r"%Y-%m-%dT%H:%M:%S.%f:%z").timestamp()
        return ts
    dataframe['time'] = dataframe.apply(toEpoch, axis=1)
    return dataframe

def binancePreprocess(dataframe):    
    #Deciding the side of the trade
    def isBuyer(row):
        if(row['isBuyerMaker']):
            return 'buy'
        else:
            return 'sell'
    
    #Converting the isBuyerMaker to buy/sell value
    dataframe['isBuyerMaker'] = dataframe.apply(isBuyer, axis=1)
    
    return dataframe

def getTrades(pair, source):
    """
        Parameters:
            pair (tuple): Consists of currency tickers being traded
            source (string): Source API
        Returns:
            dataframe: The trades dataframe related to product_id at that time or an error message
            or
            string: if an error occurs
    """
    META_DATA = {
        'Coinbase': {
            'url': 'https://api.pro.coinbase.com/products/' + pair[0]+'-'+pair[1] + '/trades',
            'cols': ['token_id', 'price', 'size', 'pair', 'trade_id', 'side', 'source', 'time'],
            'product_id': pair[0]+'-'+pair[1],
            'preprocess': coinbasePreprocess,
            'params': {}
        },

        'Binance': {
            'url': 'https://api.binance.com/api/v3/trades?symbol=' + pair[0]+pair[1],
            'cols': ['token_id', 'price', 'qty', 'pair', 'id', 'isBuyerMaker', 'source', 'time'],
            'product_id': pair[0]+pair[1],
            'preprocess': binancePreprocess,
            'params': {}
        }
    }


    final_cols = ['token_id', 'price', 'size', 'pair', 'trade_id', 'side', 'source', 'time']
    token_id = pair[0]
    cols = META_DATA[source]['cols']
    url = META_DATA[source]['url']
    product_id = META_DATA[source]['product_id']
    preprocess = META_DATA[source]['preprocess']
    params = META_DATA[source]['params']

    #Making a request
    r = requests.get(url = url)
    data = r.json()

    #Return dataframe if the request is successful
    if(r.status_code==200):
        #Type casting size and price to float
        df = pd.DataFrame(data).astype({cols[2]: np.float64, cols[1]: np.float64, cols[4]: np.int64})
        
        #Source specific preprocessing
        df = preprocess(df)

        #Setting pair, source and token_id
        df['pair'] = product_id
        df['token_id'] = token_id
        df['source'] = source
        df = df[cols]

        #Changing column names
        df.columns = final_cols
        return df
    #Handling case when an empty is acquired
    elif(len(data) == 0):
        print("No records to be shown!")
    else:
        # error_message = str(r.status_code) + " " + data['message']
        error_message = ""
        return "ERROR: " + error_message


if(__name__ == '__main__'):
    print(getTrades(('BTC', 'USDT'), 'Binance'))