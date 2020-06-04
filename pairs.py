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

    cols = ['id', 'base_currency', 'quote_currency']
    URL = "https://api.pro.coinbase.com/products/"
    # pair = product_id.split('-')

    #Making request
    r = requests.get(url = URL)
    data = r.json()
    
    #Creating the dataframe
    if(r.status_code == 200):
        #Filtering columns
        pair_df = pd.DataFrame(data)[cols]
        pair_df['exchange'] = source
        
        #Changing column names
        pair_df.columns = ['product_id', 'asset', 'currency', 'exchange']
        return pair_df
    elif(len(data) == 0):
        print("No records to be shown!")
    else:
        error_message = str(r.status_code) + " " + data['message']
        return "Error: " + error_message

if(__name__ == '__main__'):
    print(getPair('Coinbase'))