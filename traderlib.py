# encoding: utf-8

# import needed libraries
import sys
from logger import *
import gvars
from pya3 import *
import time
import yfinance as yf

class Trader:
    def __init__(self, ticker, api):
        # Initialize with ticker and api

        lg.info('Trader initialized with ticker %s' % ticker)
        self.ticker = ticker
        self.api = api

    def set_stoploss(self, entryPrice, trend):
        # takes an entry price and sets the stoploss (trend)
            # IN: entry price, trend (long/short)
            # OUT: stop loss ($)

        try:
            if trend == 'long':
                # example: 10 - (10*0.05) = 9.5
                stopLoss = entryPrice - (entryPrice * gvars.stopLossMargin)
                lg.info('Stop loss set for long at %.2f' % stopLoss)
                return stopLoss
            elif trend == 'short':
                # example: 10 + (10*0.05) = 10.5
                stopLoss = entryPrice + (entryPrice * gvars.stopLossMargin)
                lg.info('Stop loss set for long at %.2f' % stopLoss)
                return stopLoss
            else:
                raise ValueError

        except Exception as e:
            lg.error('The trend value is not understood: %s' % str(trend))
            sys.exit()

    def set_takeprofit(self, entryPrice, trend):
        # takes a price as an input and sets the takeprofit
            # IN: entry price, trend (long/short)
            # OUT: take profit ($)

        try:
            if trend == 'long':
                # example: 10 + (10*0.1) = 11$
                takeProfit = entryPrice + (entryPrice * gvars.takeProfitMargin)
                lg.info('Take profit set for long at %.2f' % takeProfit)
                return takeProfit
            elif trend == 'short':
                # example: 10 - (10*0.1) = 9$
                takeProfit = entryPrice - (entryPrice * gvars.takeProfitMargin)
                lg.info('Take profit set for short at %.2f' % takeProfit)
                return takeProfit
            else:
                raise ValueError

        except Exception as e:
            lg.error('The trend value is not understood: %s' % str(trend))
            sys.exit()

    def load_historical_data(self, ticker, interval, period):
        # load historical stock data
            # IN: ticker, interval (aggregation), api, entries limit
            # OUT: array with stock data (OHCL)

        try:
            # load data from broker or yahoo finance
            lg.info('Loading data ...')
            # from yahoo finance
            ticker = ticker + '.NS'
            ticker = yf.Ticker(ticker)
            data = ticker.history(period, interval)
        except Exception as e:
            lg.error('Something happened while loading historical data')
            lg.error(e)
            sys.exit()
        return data

    def submit_order(self, trend, ticker, sharesQty, exit = False):
        # IN: order data (number of shares, order type)
        # OUT: boolean (True = order went through, False = order did not)

        lg.info('Submitting %s Order for %s' % (trend, ticker))
        currentPrice = 0.0
        if trend == 'long' and not exit:
            side = TransactionType.Buy
            limitPrice = round(currentPrice + currentPrice * gvars.maxVar, 2)
        elif trend == 'short' and not exit:
            side = TransactionType.Sell
            limitPrice = round(currentPrice - currentPrice * gvars.maxVar, 2)
        elif trend == 'long' and exit:
            side = TransactionType.Sell
        elif trend == 'short' and exit:
            side = TransactionType.Buy
        else:
            lg.error('Trend was not understood')
            sys.exit()
        try:
            lg.info('Current price: %.2f' % currentPrice)
            order = self.api.place_order(transaction_type = side,
                instrument = self.api.get_instrument_by_symbol('NSE', ticker),
                quantity = sharesQty,
                order_type = OrderType.Market,
                product_type = ProductType.Intraday,
                price = 0.0,
                trigger_price = None,
                stop_loss = None,
                square_off = None,
                trailing_sl = None,
                is_amo = False,
                order_tag ='order1')

            lg.info('order response: %s' % order)
            self.orderId = order['NOrdNo']
            lg.info('%s order submitted correctly!' % trend)
            lg.info('%d shares %s for %s' % (sharesQty, side, ticker))
            lg.info('order ID: %s' % self.orderId)
            return True

        except Exception as e:
            lg.error('Something happend when submitting order')
            lg.error(str(e))
            sys.exit()

    def cancel_pending_order(self, ticker):
        # cancel order: cancels our order (retry)
            # IN: order id
            # OUT: boolean (True = order cancelled, False = order not cancelled)
        lg.info('Order %s cancelled correctly' % self.orderId)
        return True

    def check_position(self, ticker, doNotFind = False):
        # check whether the position exists or not
            # IN: ticker, doNotFind (means that I dont want to find)
            # OUT: boolean (True = order is there, False = order not there)
        lg.info('The position was found, for %s ' % ticker)

    def get_shares_amount(self, assetPrice):
        # works out the number of shares I want to buy/sell
            # IN: assetPrice
            # OUT: number of shares

        lg.info('Getting shares amount')
        return 1

    def get_avg_entry_price(self, ticker):
        # get the average price of an ticker with a position open
            # IN: ticker
            # OUT: price ($)
        avgEntryPrice = 100.0
        lg.info('The position was checked. average price is: %.2f' % avgEntryPrice)
        return avgEntryPrice

    def get_general_trend(self, ticker):
        # get general trend: detect interesting trend (UP / DOWN / FALSE if not trend)
            # IN: ticker
            # OUTPUT: LONG / SHORT / NO TREND (strings)
            #If no trend defined, go back to POINT ECHO

        lg.info('General Trend analysis entered')
        lg.info('------------------------------------ \n')

        data = self.load_historical_data(ticker, interval = '5m', period = '3H')
        print(data)
        # return False

        try:
            # this is for test purpose only
            lg.info('Trend detected for %s: long \n' % ticker)
            return 'long'

        except Exception as e:
            lg.error('Something went wrong at get general trend')
            lg.error(e)
            sys.exit()

    def get_instant_trend(self, ticker, trend):
        # get instat trend: confirm the trend detected by GT analysis
            # IN: ticker, trend (long / short)
            # OUT: True (trend confirmed) / False (not a good moment to enter)

        lg.info('instat Trend analysis entered')
        lg.info('------------------------------------ \n')

        try:
            # this is for test purpose only
            lg.info('Trend detected for %s: %s \n' % (ticker, trend))
            return True

        except Exception as e:
            lg.error('Something went wrong at get instant trend')
            lg.error(e)
            sys.exit()

    def enter_position_mode(self, ticker, trend):
        # check the conditions in parallel once inside the position
        # depending on the trend
            # IN: ticker, trend
            # OUT: True if Success / False if Fail/Time out

        try:
            pass
        except Exception as err:
            pass
        return True

    def run(self):
        # check the trends in parallel once confirm tred enter position mode
        # depending on the trend take tarde
        # IN: ticker
        # OUT: True if Success / False if Fail/Time out

        lg.info('Running trade for %s' % self.ticker)

        #POINT ECHO: LOOP until timeout reached (ex. 2h)
        while True:
            # find general a trend
            trend = self.get_general_trend(self.ticker)
            if not trend:
                lg.info('No general trend found for %s! Going out...' % self.ticker)
                return False # aborting execution

        successfulOperation = True

        # end of execution
        lg.info('\nDONE: end of execution ...!!')
        lg.info('----------------------------- \n')
        return successfulOperation
