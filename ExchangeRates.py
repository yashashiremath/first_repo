import requests
import sys

def getExchangeRate(from_curr, to_curr):
    """
    Parameters:
        from_curr (str) : Original currency code (eg. EUR)
        to_curr (str) : Exchange currency to which the original currency to be converted
        
    Returns:
        float : Exchage rate to convert the currency
    """
    
    #URL for current exchange rates
    URL = 'https://api.coinbase.com/v2/exchange-rates?currency='+from_curr
    r = requests.get(url = URL)
    data = r.json()
    if(r.status_code == 200):
        if(to_curr in data['data']['rates'].keys()):
            return float(data['data']['rates'][to_curr])
        else:
            print("Error: Quote currency not valid")
            sys.exit()
    else:
        import pdb; pdb.set_trace()
        error_message = str(r.status_code) + " " + str(data['errors'][0])
        return "Error: " + error_message

if __name__ == '__main__':
    print(getExchangeRate('BTC', 'USD'))