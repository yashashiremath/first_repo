import requests
import pandas as pd

def getStats(product_id):
    """
        Parameters:
            product_id (string): Consists of crypto-currency and fiat currency tickers ex: BTC-USD
        Returns:
            Series: A pandas series of stats for the product_id

    """

    cols = ['symbol', 'volume', 'lowPrice', 'highPrice', 'openPrice']
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    r = requests.get(url=url)

    if(r.status_code == 200):
        #Getting data
        data = r.json()

        #Creating Dataframe
        stats_df = pd.DataFrame(data)[cols]
        stats_df.columns = ['product_id', 'volume', 'high', 'low', 'open']
        return stats_df
    else:
        return "Error: " + str(r.status_code) 

if(__name__ == '__main__'):
    print(getStats('BTCUSDT'))