# encoding: utf-8

# import needed libraries
import configparser
from traderlib import *
from logger import *
from pya3 import *

def get_user_info():
    # get user info from user for login and authentication.
        # IN: (from user)
        # OUT: True Once successful and exiting otherwise
    lg.info('getting user info ...')
    gvars.USERNAME = input("Enter USERNAME \n")
    gvars.API_KEY = input("Enter API KEY \n")

    config_path = './config/'
    config_obj = configparser.ConfigParser()
    config_file = config_path + "config.ini"

    config_obj.add_section('user_info')
    config_obj.set('user_info', 'USERNAME', gvars.USERNAME)
    config_obj.set('user_info', 'API_KEY', gvars.API_KEY)

    # creating s folder for the config
    try:
        os.mkdir(config_path)
    except OSError:
        lg.info('Creation of the directory %s failed - it does not have to be bad' % config_path)
    except Exception as err:
        lg.error(str(err))
        sys.exit()
    else:
        lg.info('Succesfully created config directory')

    # Write the new structure to the new file
    with open(config_file, 'w') as configfile:
        config_obj.write(configfile)

# initialize bot for trading account
def initialize_bot():
    # initialize the bot
        # IN: None
        # OUT: True initialize successful and exiting otherwise

    lg.info('Initializing BOT ...')
    config_path = './config/'
    config_obj = configparser.ConfigParser()
    config_file = config_path + "config.ini"

    try:
        config_obj.read(config_file)
        userinfo = config_obj["user_info"]
        gvars.USERNAME = userinfo['username']
        gvars.API_KEY = userinfo['api_key']
        lg.info('\nAccount USERNAME: %s, KEY: %s ...' %(gvars.USERNAME, gvars.API_KEY))
    except KeyError as err:
        get_user_info()
    except Exception as err:
        lg.error(str(err))
        sys.exit()

    try:
        config_obj.read(config_file)
        userinfo = config_obj["user_info"]
    except Exception as err:
        lg.error(str(err))
        sys.exit()

    lg.info('Initializing BOT Successfull')
    return True

# check our trading account
def check_account_ok(api):
    # check whether the account is Active for trading
        # IN: api
        # OUT: True if it exists and is Active / False otherwise

    try:
        session_id = api.get_session_id() # Get Session ID
        lg.info('session_id: %s ' % str(session_id))
        if session_id['stat'] != 'Ok':
            if('ConnectionError' in str(session_id['emsg'])):
                lg.error('\nConnection error. Please check the speed of the Internet')
                lg.error('\n%s ' % session_id)
                sys.exit()
            lg.info('\nThe account is not ACTIVE, aborting')
            sys.exit()
        else:
            if 'emsg' in session_id:
                lg.error('\n%s ' % session_id['emsg'])
                sys.exit()
    except Exception as e:
        lg.error('\nCould not get account info, aborting')
        lg.error(str(e))
        sys.exit()

    lg.info('\nThe account is ACTIVE, Good to go ...')
    lg.info('Generated session_id, session_id: %s ' % session_id)

# close current orders
def clean_open_orders(api):
    # check whether any orders is Active or Not
        # IN: api
        # OUT: True if it exists and is cleared / False otherwise

    try:
        # if No data found then return from api = {'emsg': 'No Data', 'stat': 'Not_Ok'}
        orderBook = api.get_order_history('')
        if (type(orderBook) == dict) and (orderBook['stat'] != 'Ok'):
            lg.error("\n%s " % orderBook['emsg'])
            sys.exit()
        for order in orderBook:
            if order['Unfilledsize'] != 0:
                cancelOrder = api.cancel_order(order['Nstordno'])
                print(cancelOrder)
    except Exception as e:
        lg.error("\nSomething went wrong while clearing open order")
        lg.error(str(e))
        sys.exit()
    lg.info('cleaned open orders, good to go !')

def check_asset_ok(api, ticker):
    # check whether the asset is OK for trading
        # IN: ticker
        # OUT: True if it exists and is tradable / False otherwise
    try:
        asset = api.get_instrument_by_symbol('NSE', ticker)
        if type(asset) == dict:
            lg.error('Asset does not exist, exiting')
            sys.exit()

        if 'EQ' in asset.name:
            lg.info('Asset exists and tradable')
            return True
        else:
            lg.info('Asset exists but not tradable, exiting')
            sys.exit()
    except Exception as e:
        lg.error('something happens!')
        lg.error(e)
        sys.exit()

def main():

    # IN: None
    # OUT: boolean tradingSuccess (True = success / False = failure)

    print('THE MAIN IS STARTED ... ')
    print('------------------------------------ \n')

    # initialize the logger (imported from logger)
    initialize_logger()

    # initialize bot
    initialize_bot()
    api = Aliceblue(user_id = gvars.USERNAME, api_key = gvars.API_KEY)

    # check our trading account
    check_account_ok(api)

    # close current orders
    clean_open_orders(api)

    # get ticker
    #ticker = input('Write the ticker you want to operate with: ')
    ticker = 'ONGC'

    check_asset_ok(api, ticker)

    trader = Trader(ticker, api) # initialize trading bot

    tradingSuccess = trader.run()
    # tradingSuccess = True

    if not tradingSuccess:
        lg.info('Trading was not successful, locking asset')
    else:
        lg.info('Trading was successful!')

    lg.info('------------------------------------')
    print('\nTHE MAIN END ...!! ')

if __name__ == '__main__':
    main()
