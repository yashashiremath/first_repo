import requests
import pandas as pd
import datetime

def getStats(product_id):
    """
        Parameters:
            product_id (string): Consists of crypto-currency and fiat currency tickers ex: BTC-USD
        Returns:
            Series: A pandas series of stats for the product_id

    """

    cols = ['volume', 'high', 'low', 'open']
    end = datetime.datetime.now()
    start = end - datetime.timedelta(hours=48)
    end = int(end.timestamp())
    start = int(start.timestamp())
    diff = end - start 
    
    URL = f"https://poloniex.com/public?command=returnChartData&currencyPair={product_id}&start={start}&period=86400"

    #Making request
    r = requests.get(url = URL)

    #Creating the series of stats if the request was successful
    if(r.status_code == 200):
        #Getting data
        data = r.json()

        import pdb; pdb.set_trace()

        stats_df = pd.DataFrame(data=data, index=[0])[cols]
        stats_df['id'] = product_id
        stats_df.columns = cols + ['product_id']
        return stats_df[['product_id', 'volume', 'high', 'low', 'open']]
    elif(len(data) == 0):
        print("No records to be shown!")
    else:
        error_message = str(r.status_code) + " " + data['message']
        return "Error: " + error_message

if(__name__ == '__main__'):
    print(getStats('BTC_XMR'))