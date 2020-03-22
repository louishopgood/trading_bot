# .data is the pandas datareader command we need get data from Yahoo
import pandas_datareader.data as pdr
# data reader meeds start and end date to be supplied in datetime format
import datetime as dt

ticker = "AMZN"
 
start_date = dt.date.today()-dt.timedelta(365)
end_date = dt.date.today()

#pandas datareader can only go down to daily data, not intr-day. To specify monthly add argument interval = "m"
data = pdr.get_data_yahoo(ticker, start_date, end_date)
