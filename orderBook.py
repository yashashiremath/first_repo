import requests
import pandas as pd 
import numpy as np 

def getOrderBook(product_id):
    """
        Parameters:
            product_id (string): Consists of crypto-currency and fiat currency tickers ex: BTC-USD
        Returns:
            Dataframe: A dataframe with details of buy and sell orders
            or
            string: if an error occurs
    """

    cols = ['price', 'size', 'num-orders']
    URL = "https://api.pro.coinbase.com/products/" + product_id + "/book?level=2"

    #Making request
    r = requests.get(url = URL)
    data = r.json()

    #Creating Sell and Buy dataframes
    if(r.status_code == 200 and ('asks' in data.keys()) and ('bids' in data.keys())):
        sell_df = pd.DataFrame(data['asks'], columns=cols)
        buy_df = pd.DataFrame(data['bids'], columns=cols)
        sell_df['side'] = 'sell'
        buy_df['side'] = 'buy'
        return sell_df.append(buy_df).reset_index()
    else:
        error_message = str(r.status_code) + " " + data['message']
        return "Error: " + error_message
    
if(__name__ == '__main__'):
    print(getOrderBook('BTC-USD'))