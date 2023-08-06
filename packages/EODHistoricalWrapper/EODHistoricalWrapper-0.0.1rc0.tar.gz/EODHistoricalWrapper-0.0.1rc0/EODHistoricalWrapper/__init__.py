import requests
import pandas as pd
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
    
class EODHistorical:
    
    class Fundamentals:
        
        class Earnings:
            def __init__(self, data):
                self.data = data
                
                self.history = pd.DataFrame(data['History'])
                self.trend = pd.DataFrame(data['Trend'])
                self.annual = pd.DataFrame(data['Annual'])
        
        class Financials:
            def __init__(self, data):
                self.data = data
                
                self.balance_sheet_quarterly = pd.DataFrame(data['Balance_Sheet']['quarterly'])
                self.balance_sheet_yearly = pd.DataFrame(data['Balance_Sheet']['yearly'])
                
                self.cash_flow_quarterly = pd.DataFrame(data['Cash_Flow']['quarterly'])
                self.cash_flow_yearly = pd.DataFrame(data['Cash_Flow']['yearly'])
                
                self.income_statement_quarterly = pd.DataFrame(data['Income_Statement']['quarterly'])
                self.income_statement_yearly = pd.DataFrame(data['Income_Statement']['yearly'])
                
        def __init__(self, api_key, symbol):
            # Get Fundamentals
            res = requests.get('https://eodhistoricaldata.com/api/fundamentals/%s?api_token=%s' % (symbol, api_key))
            if res.status_code == 404:
                raise KeyError('Symbol not Found.')
            if (res.status_code >= 300) | (res.status_code < 200):
                raise ConnectionError('Connection Error')
            
            data = res.json()
            
            self.general = data['General']
            self.highlights = data['Highlights']
            self.valuation = data['Valuation']
            self.sharesstats = data['SharesStats']
            self.technicals = data['Technicals']
            self.splitsdividends = data['SplitsDividends']
            
            self.earnings = EODHistorical.Fundamentals.Earnings(data['Earnings'])
            self.financials = EODHistorical.Fundamentals.Financials(data['Financials'])
        
    class Historical:
        def __init__(self, api_key, symbol):
            res = requests.get('https://eodhistoricaldata.com/api/shorts/%s?api_token=%s' % (symbol, api_key))
            if res.status_code == 404:
                raise KeyError('Symbol not Found.')
            if (res.status_code >= 300) | (res.status_code < 200):
                raise ConnectionError('Connection Error')
            
            self.short_interest = pd.read_csv(StringIO(res.text))[:-1]
            
            res = requests.get('https://eodhistoricaldata.com/api/div/%s?api_token=%s' % (symbol, api_key))
            if res.status_code == 404:
                raise KeyError('Symbol not Found.')
            if (res.status_code >= 300) | (res.status_code < 200):
                raise ConnectionError('Connection Error')
            
            self.dividends = pd.read_csv(StringIO(res.text))[:-1]
            
            res = requests.get('https://eodhistoricaldata.com/api/splits/%s?api_token=%s' % (symbol, api_key))
            if res.status_code == 404:
                raise KeyError('Symbol not Found.')
            if (res.status_code >= 300) | (res.status_code < 200):
                raise ConnectionError('Connection Error')
            
            self.splits = pd.read_csv(StringIO(res.text))[:-1]
            
            res = requests.get('https://eodhistoricaldata.com/api/eod/%s?api_token=%s' % (symbol, api_key))
            if res.status_code == 404:
                raise KeyError('Symbol not Found.')
            if (res.status_code >= 300) | (res.status_code < 200):
                raise ConnectionError('Connection Error')
            
            self.prices = pd.read_csv(StringIO(res.text))[:-1]
            
    def __init__(self, api_key, symbol):
        self.fundamentals = EODHistorical.Fundamentals(api_key, symbol)
        self.historical = EODHistorical.Historical(api_key, symbol)