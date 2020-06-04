import requests
import pandas as pd

def getStats(product_id):
    """
        Parameters:
            product_id (string): Consists of crypto-currency and fiat currency tickers ex: BTC-USD
        Returns:
            Series: A pandas series of stats for the product_id

    """

    cols = ['id', 'volume', 'high', 'low', 'open']
    URL = f"https://api.pro.coinbase.com/products/{product_id}/stats"

    #Making request
    r = requests.get(url = URL)
    data = r.json()

    #Creating the series of stats if the request was successful
    if(r.status_code == 200):
        stats_df = pd.DataFrame(data=data, index=[0])
        stats_df['id'] = product_id
        return stats_df[cols]
    elif(len(data) == 0):
        print("No records to be shown!")
    else:
        error_message = str(r.status_code) + " " + data['message']
        return "Error: " + error_message

if(__name__ == '__main__'):
    print(getStats('BTC-USD'))