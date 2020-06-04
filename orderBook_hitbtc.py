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
    URL = f"https://api.hitbtc.com/api/2/public/orderbook"

    #Making request
    r = requests.get(url = URL)

    #Creating Sell and Buy dataframes
    if(r.status_code == 200):
        #Getting data
        data = r.json()[product_id]

        #Creating Dataframe
        sell_df = pd.DataFrame(data['ask'], columns=cols)
        buy_df = pd.DataFrame(data['bid'], columns=cols)
        sell_df['side'] = 'sell'
        buy_df['side'] = 'buy'

        #Resetting index
        final_df = sell_df.append(buy_df).reset_index()
        final_df.index = final_df['index']
        final_df.drop(columns=['index'], inplace=True)
        return final_df
    else:
        return "Error: " + str(r.status_code)
    
if(__name__ == '__main__'):
    print(getOrderBook('FXTETH'))