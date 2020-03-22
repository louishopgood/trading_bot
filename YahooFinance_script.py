# ============================================================================
# Import OHLCV data using yahoofinancials
# Author - Mayank Rasu
# =============================================================================


import pandas as pd
from yahoofinancials import YahooFinancials
import datetime

all_tickers = ["AAPL","MSFT","CSCO","AMZN","INTC"]

# extracting stock data (historical close price) for the stocks identified
close_prices = pd.DataFrame()
end_date = (datetime.date.today()).strftime('%Y-%m-%d')
beg_date = (datetime.date.today()-datetime.timedelta(1825)).strftime('%Y-%m-%d')
cp_tickers = all_tickers
attempt = 0
drop = []
while len(cp_tickers) != 0 and attempt <=5:
    print("-----------------")
    print("attempt number ",attempt)
    print("-----------------")
    cp_tickers = [j for j in cp_tickers if j not in drop]
    for i in range(len(cp_tickers)):
        try:
            yahoo_financials = YahooFinancials(cp_tickers[0])
            #gets the historical data in json form
            json_obj = yahoo_financials.get_historical_price_data(beg_date,end_date,"daily")
            #json_object is a dictionary with a key called prices with a list of dictionaries, each containing OHCLV data for the different dates            
            ohlv_data = json_obj[cp_tickers[0]]['prices']
            #makes a datafram which just contains the date and adj code for current stock
            #a feature of dataframes is if you feed it a list of dictionaries, the keys of the dictionaries will become the columns of the dataframe
            temp = pd.DataFrame(ohlv_data)[["formatted_date","adjclose"]]
            #replaces the 0-xxxx index, the date column is used as the index of the dataframe
            temp.set_index("formatted_date",inplace=True)
            #duplicated returns list of bools to say if is a duplicate or not. keep ="first" means the first of each duplicate is recorded as false
            # ~ swaps true for false and vise versa, so end up with True on the ones we want to keep.
            # then when we do temp[(list of bools)] it only stores the ones that are True and so not duplicates
            temp2 = temp[~temp.index.duplicated(keep='first')] 
            close_prices[cp_tickers[i]] = temp2["adjclose"]
            drop.append(cp_tickers[i])       
        except:
            print(cp_tickers[i]," :failed to fetch data...retrying")
            continue
    attempt+=1