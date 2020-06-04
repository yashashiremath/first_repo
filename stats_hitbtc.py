import requests
import pandas as pd

def getStats(product_id):
    """
        Parameters:
            product_id (string): Consists of crypto-currency and fiat currency tickers ex: BTC-USD
        Returns:
            Series: A pandas series of stats for the product_id

    """

    cols = ['symbol', 'volume', 'high', 'low', 'open']
    URL = f"https://api.hitbtc.com/api/2/public/tickers"

    #Making request
    r = requests.get(url = URL)

    #Creating the series of stats if the request was successful
    if(r.status_code == 200):
        #Get data
        data = r.json()

        #Creating dataframe
        stats_df = pd.DataFrame(data=data)[cols]
        stats_df.columns = ['product_id', 'volume', 'high', 'low', 'open']
        return stats_df
    else:
        return "Error: " + str(r.status_code)

if(__name__ == '__main__'):
    print(getStats('BTC-USD'))