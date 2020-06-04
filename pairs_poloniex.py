import requests
import pandas as pd
import numpy as np

def getPair(source):
    """
        Parameters:
            source (string): Source API
        Returns:
            Series: A pandas dataframe with the pair details
            or
            string: if an error occurs
    """

    cols = ['product_id', 'asset', 'currency', 'exchange']
    URL = "https://poloniex.com/public?command=returnTicker"
    # pair = product_id.split('-')

    #Making request
    r = requests.get(url = URL)

    #Creating the dataframe
    if(r.status_code == 200):
        #Getting data
        data = r.json()
        symbols = data.keys()

        pair_df = pd.DataFrame(data=symbols, columns=['product_id'])
        pair_df['asset'] = pair_df.apply(lambda row: row['product_id'].split('_')[1], axis=1)
        pair_df['currency'] = pair_df.apply(lambda row: row['product_id'].split('_')[0], axis=1)
        pair_df['exchange'] = source

        #Rearranging columns
        return pair_df[cols]
    else:
        return "Error: " + str(r.status_code)

if(__name__ == '__main__'):
    print(getPair('Poloniex'))