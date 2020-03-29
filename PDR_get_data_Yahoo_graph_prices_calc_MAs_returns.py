 # =============================================================================
# Import OHLCV data using Pandas Datareader
# =============================================================================
#this script gets around the problem of one of the API connections failing and causing the entire data import to stop meaning the algorithm would fail
# Import necesary libraries
import pandas as pd
import pandas_datareader.data as pdr
import datetime
from matplotlib import pyplot as plt

# Download historical data for NIFTY constituent stocks
tickers = ["MSFT","AMZN","AAPL","CSCO","IBM","FB"]

stock_cp = pd.DataFrame() # dataframe to store close price of each ticker
attempt = 0 # initializing passthrough variable
extracted_succesfully = [] # initializing list to store tickers whose close price was successfully extracted
failed_list = []
while len(tickers) != 0 and attempt <= 5: #will only loop through a maximum of 5 times, if not limited will cause stack overflow if even 1 API returns an error
    #this list concetation loops through tickers only keeping the stocks that are not in the drop list
    #the w hile loop runs a maximum of 5 times, stopping if all APIs are successfully accessed
    tickers = [j for j in tickers if j not in extracted_succesfully] # removing stocks whose data has been extracted from the ticker list
    #the for loop runs through each stock that the updated tickers list contains 
    for i in range(len(tickers)):
        # tries to open API connection for current ticker
        try:
            #creates a temp variable which is the OCHLV data for that stock between the start and end datetimes from Yahoo Finance
            temp = pdr.get_data_yahoo(tickers[i],datetime.date.today()-datetime.timedelta(10000),datetime.date.today())
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
    
stock_cp.fillna(method = "bfill", inplace = True, axis = 0)  
 #we would rather fill in the NaN values, we here do a backfill so the values before a stock is listed is just its opening price
 #its daily return would therefore be zero
 
#stock_cp.dropna(axis=0, inplace = False) #if it finds an NaN it deletes that row as axis = 0 not 1. This makes a copy and doesnt
 #replace the dataframe as inplace = False. You would lose data for the other stocks if you just did dropna here.
 
plt.figure(figsize = (12, 8))
ax1 = plt.subplot(2,3,1)
stock_cp["AAPL"].plot()
plt.title("AAPL")

ax2 = plt.subplot(2,3,2)
stock_cp["AMZN"].plot()
plt.title("AMZN")

ax3 = plt.subplot(2,3,3)
stock_cp["MSFT"].plot()
plt.title("MSFT")

ax4 = plt.subplot(2,3,4)
stock_cp["CSCO"].plot()
plt.title("CSCO")

ax5 = plt.subplot(2,3,5)
stock_cp["IBM"].plot()
plt.title("IBM")

ax6 = plt.subplot(2,3,6)
stock_cp["FB"].plot()
plt.title("FB")

plt.tight_layout()

 #Mean, Median, Standard Deviation, Daily Return
stock_cp.mean()
stock_cp.median()
stock_cp.std()

daily_return = stock_cp.pct_change()
(((stock_cp/stock_cp.shift(1))-1)) == daily_return # two ways of getting daily returns

#.shift() shifts the whole dataframe down by what you specify
print("Mean Daily Return: ")
print(daily_return.mean())
print("Standard Deviation of Returns: ")
print(daily_return.std())

#rolling mean and standard deviation - e.g. how does the 20 day mean change over the time period
daily_return.rolling(window = 20, min_periods = 20).mean()  #this calculates a 20 day rolling mean for each stock
#if over a few months the rolling mean has been rising then it is a good indication of positive movement in the stock
#min periods sets the min number of values needed to display an average. Here, the 2nd date has a MA value even though it is not a 20 day moving average but a two day one
#The first 20 values are not 20-day MA's but are averages of the number of data points then available.
daily_return.rolling(window = 20, min_periods = 20).std()

#exponential MA gives more weight to the more recent dates
daily_return.ewm(span = 20, min_periods = 20).mean()
daily_return.ewm(span = 20, min_periods = 20).std()