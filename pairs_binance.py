import requests
import pandas as pd 

def getPairs(source):
    """
        Parameters:
            source (string): Source API
        Returns:
            Series: A pandas dataframe with the pair details
            or
            string: if an error occurs
    """
    
    cols = ['symbol', 'baseAsset', 'quoteAsset']
    url = "https://api.binance.com/api/v1/exchangeInfo"

    r = requests.get(url=url)

    if(r.status_code == 200):
        #Getting data
        data = r.json()
        data = data['symbols']

        #Creating dataframe
        pair_df = pd.DataFrame(data)[cols]
        pair_df['source'] = 'Bincance'
        return pair_df
    else:
        return "Error: " + str(r.status_code) 



if(__name__ == '__main__'):
    print(getPairs('Binance'))