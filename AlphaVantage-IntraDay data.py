# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:04:57 2020

@author: louis
"""

from alpha_vantage.timeseries import TimeSeries


ts = TimeSeries("J8TRIDMULCVPLH4Y", output_format="pandas")
data, meta_data = ts.get_intraday(symbol = "MSFT", interval="1min", outputsize="full")

            
        

    
    
    
    
