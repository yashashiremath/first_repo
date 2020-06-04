import requests
import pandas as pd 

def getPair(source):
    """
        Parameters:
            source (string): Source API
        Returns:
            Series: A pandas dataframe with the pair details
            or
            string: if an error occurs
    """

    cols = ['id', 'baseCurrency', 'quoteCurrency']
    URL = "https://api.hitbtc.com/api/2/publidc/symbol"
    # pair = product_id.split('-')

    #Making request
    r = requests.get(url = URL)
    
    #Creating the dataframe
    if(r.status_code == 200):
        #Getting data
        data = r.json()

        #Filtering columns
        pair_df = pd.DataFrame(data)[cols]
        pair_df['exchange'] = source
        
        #Changing column names
        pair_df.columns = ['product_id', 'asset', 'currency', 'exchange']
        return pair_df
    else:
        return "Error: " + str(r.status_code)

if(__name__ == '__main__'):
    print(getPair('HitBtc'))