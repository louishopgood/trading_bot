
#uses webscraping instead of API access, versatile way of extracting data

from yahoofinancials import YahooFinancials
import datetime as dt

ticker = "AAPL"
yahoo_financials = YahooFinancials(ticker)

historical_prices = yahoo_financials.get_historical_price_data("2019-01-01",str(dt.date.today()),"weekly")
