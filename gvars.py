# encoding: utf-8

# REST API
API_KEY = ""
USERNAME = ""

stopLossMargin = 0.01 # percentage margin for the stop loss
# example: 10 - (10*0.05) = 9.5 means that my stoploss is at 9.5$

takeProfitMargin = 0.01 # percentage margin for the take profit
# example: 10 + (10*0.1) = 11 means that my take profit is at 11$

maxSpentEquity = 5000 # total equity to spend in a single operation

# LIMIT PRICES
maxVar = 0.02 # max variation percentage when buying/selling

# MAX ATTEMPTS SECTION
maxAttemptsTT = 2160

# SLEEP TIMES SECTION (seconds)
sleepTime = 10 # MAIN EXECUTION AFTER FAILING
