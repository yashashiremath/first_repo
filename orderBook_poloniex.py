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

    cols = ['price', 'size']
    URL = f"https://poloniex.com/public?command=returnOrderBook&currencyPair={product_id}&depth=50"

    #Making request
    r = requests.get(url = URL)

    #Creating Sell and Buy dataframes
    if(r.status_code == 200):
        #Getting data
        data = r.json()

        #Creating Dataframe
        sell_df = pd.DataFrame(data['asks'], columns=cols)
        buy_df = pd.DataFrame(data['bids'], columns=cols)
        sell_df['side'] = 'sell'
        buy_df['side'] = 'buy'

        #Resetting index
        final_df = sell_df.append(buy_df)
        final_df.index = range(len(final_df))
        return final_df
    else:
        return "Error: " + str(r.status_code)
    
if(__name__ == '__main__'):
    print(getOrderBook('BTC_ETH'))