# =============================================================================
# Import OHLCV data using Pandas Datareader
# =============================================================================
#this script gets around the problem of one of the API connections failing and causing the entire data import to stop meaning the algorithm would fail
# Import necesary libraries
import pandas as pd
import pandas_datareader.data as pdr
import datetime

# Download historical data for NIFTY constituent stocks
tickers = ["ASIANPAINT.NS","ADANIPORTS.NS","AXISBANK.NS","BAJAJ-AUTO.NS",
           "BAJFINANCE.NS","BAJAJFINSV.NS","BPCL.NS","BHARTIARTL.NS",
           "INFRATEL.NS","CIPLA.NS","COALINDIA.NS","DRREDDY.NS","EICHERMOT.NS",
           "GAIL.NS","GRASIM.NS","HCLTECH.NS","HDFCBANK.NS","HEROMOTOCO.NS",
           "HINDALCO.NS","HINDPETRO.NS","HINDUNILVR.NS","HDFC.NS","ITC.NS",
           "ICICIBANK.NS","IBULHSGFIN.NS","IOC.NS","INDUSINDBK.NS","INFY.NS",
           "KOTAKBANK.NS","LT.NS","LUPIN.NS","M&M.NS","MARUTI.NS","NTPC.NS",
           "ONGC.NS","POWERGRID.NS","RELIANCE.NS","SBIN.NS","SUNPHARMA.NS",
           "TCS.NS","TATAMOTORS.NS","TATASTEEL.NS","TECHM.NS","TITAN.NS",
           "UPL.NS","ULTRACEMCO.NS","VEDL.NS","WIPRO.NS","YESBANK.NS","ZEEL.NS"]

stock_cp = pd.DataFrame() # dataframe to store close price of each ticker
attempt = 0 # initializing passthrough variable
extracted_succesfully = [] # initializing list to store tickers whose close price was successfully extracted
failed_list = []
while len(tickers) != 0 and attempt <= 5: #will only loop through a maximum of 5 times, if not limited will cause stack overflow if even 1 API returns an error
    #this list concetation loops through tickers only keeping the stocks that are not in the drop list
    #the while loop runs a maximum of 5 times, stopping if all APIs are successfully accessed
    tickers = [j for j in tickers if j not in extracted_succesfully] # removing stocks whose data has been extracted from the ticker list
    #the for loop runs through each stock that the updated tickers list contains 
    for i in range(len(tickers)):
        # tries to open API connection for current ticker
        try:
            #creates a temp variable which is the OCHLV data for that stock between the start and end datetimes from Yahoo Finance
            temp = pdr.get_data_yahoo(tickers[i],datetime.date.today()-datetime.timedelta(1095),datetime.date.today())
            # .dropna eliminates any rows (by default) that contain a NaN or None
            temp.dropna(inplace = True)
            #adds an item to the close price dataframe which will have the column heading as the ticker name and the column will contain the Adjusted Closing Prices
            stock_cp[tickers[i]] = temp["Adj Close"]
            #adds the stock to the list of succesfully extracted stocks so that if the while loop needs to repeat it will not re-access the stocks already extracted
            extracted_succesfully.append(tickers[i])    
        #if there is an error when accessing the API of the for loops current stock then it will print a retry message and then continue to the next stock
        #since if the try fails the current stock will not be on the succesfully extracted list the while loop will re-try including that stock 
        except:
            print(tickers[i]," :failed to fetch data...retrying")
            failed_list.append(tickers[i]+": pass-through "+str(attempt))
            continue
    
    print(failed_list)
    print(stock_cp)
    attempt+=1
    
 