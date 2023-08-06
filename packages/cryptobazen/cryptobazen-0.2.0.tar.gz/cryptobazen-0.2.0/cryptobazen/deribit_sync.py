import requests
import random
import hmac
import hashlib
import time


class Deribit(object):

    def __init__(self, client_id, client_secret, test_mode=False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://test.deribit.com/api/v2' if test_mode else 'https://www.deribit.com/api/v2'
        self.base_wss = 'wss://test.deribit.com/ws/api/v2' if test_mode else 'wss://www.deribit.com/ws/api/v2'
        self.session = requests.Session()

    def api_query(self, method, params, endpoint, body=""):
        # Create a signature according to the deribit documentation and create a header for all requests.
        timestamp = int(time.time() * 1000)
        nonce = ''.join([str(random.randint(0, 9)) for i in range(8)])
        string_to_sign = f'{timestamp}\n{nonce}\n{method}\n/api/v2{endpoint}?{params}\n{body}\n'
        signature = hmac.new(bytes(self.client_secret, 'utf8'), bytes(string_to_sign, 'utf8'), digestmod=hashlib.sha256).hexdigest()
        headers = {'Authorization': f'deri-hmac-sha256 id={self.client_id},ts={timestamp},nonce={nonce},sig={signature}'}

        if method == 'POST':
            response = self.session.post(f'{self.base_url}{endpoint}', data=params, headers=headers)
        elif method == 'GET':
            response = self.session.get(f'{self.base_url}{endpoint}?{params}', headers=headers)
        elif method == 'DELETE':
            response = self.session.delete(f'{self.base_url}{endpoint}', data=params, headers=headers)
        elif method == 'PUT':
            response = self.session.put(f'{self.base_url}{endpoint}', data=params, headers=headers)
        else:
            response = {'code': 999, 'msg': 'Invalid requests method. Choose POST, GET, DELETE or PUT.'}

        return response.json()['result']

    def public_auth(self):
        """
        Retrieve an Oauth access token, to be used for authentication of 'private' requests.
        :return: Oauth access token
        """
        endpoint = '/public/auth'
        params = ''
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_instruments(self, currency: str, kind: str, expired: str):
        """
        Retrieves available trading instruments. This method can be used to see which instruments are available for trading,
        or which instruments have existed historically.
        :param currency: BTC or ETH.
        :param kind: future or option
        :param expired: true or false. Means if the future or option is still open or not
        :return: Instrument data
        """
        endpoint = '/public/get_instruments'
        params = f'currency={currency}&kind={kind}&expired={expired}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_instrument(self, instrument_name: str):
        """
        Retrieves information about instrument
        :param instrument_name: BTC or ETH.
        :return: Instrument data
        """
        endpoint = '/public/get_instrument'
        params = f'instrument_name={instrument_name}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_book_summary_by_instrument(self, instrument_name: str):
        """
        Retrieves the summary information such as open interest, 24h volume, etc. for a specific instrument.
        :param instrument: The name of the option or future
        :return: book summary info
        """
        endpoint = '/public/get_book_summary_by_instrument'
        params = f'instrument_name={instrument_name}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_historical_volatility(self, currency: str):
        """
        Provides information about historical volatility for given cryptocurrency.
        :param currency: BTC or ETH.
        :return: Volatility data
        """
        endpoint = '/public/get_historical_volatility'
        params = f'currency={currency}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_last_trades(self, instrument_name: str):
        """
        Retrieve the latest trades that have occurred for a specific instrument.
        :param instrument_name: currency: BTC or ETH.
        :return: latest data with trades of a instrument
        """
        endpoint = '/public/get_last_trades_by_instrument'
        params = f'instrument_name={instrument_name}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_order_book(self, instrument_name: str, depth: int):
        """
        Retrieves the order book, along with other market values for a given instrument.
        :param instrument_name: The instrument name for which to retrieve the order book, see getinstruments to obtain instrument names
        :param depth:  	The number of entries to return for bids and asks.
        :return: Orderbook of the given instrument
        """
        endpoint = '/public/get_order_book'
        params = f'instrument_name={instrument_name}&depth={depth}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_ticker(self, instrument_name: str):
        """
        Get ticker for an instrument.
        :param instrument_name: The name of the option or future
        :return: a response with all information about the questioned instrument
        """
        endpoint = '/public/ticker'
        params = f'instrument_name={instrument_name}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def public_get_tradingview_chart_data(self, instrument_name: str, start_timestamp: int, end_timestamp: int, resolution: str):
        """
        Publicly available market data used to generate a TradingView candle chart.
        :param instrument_name: Instrument name
        :param start_timestamp: The earliest timestamp to return result for
        :param end_timestamp: The most recent timestamp to return result for
        :param resolution: Chart bars resolution given in full minutes or keyword 1D (only some specific resolutions are supported)
        :return: json with candles
        """
        endpoint = '/public/get_tradingview_chart_data'
        params = f'instrument_name={instrument_name}&start_timestamp={start_timestamp}&end_timestamp={end_timestamp}&resolution={resolution}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_get_deposits(self, currency, count=10, offset=0):
        """
        Retrieve the latest users deposits
        :param currency: BTC or ETH.
        :param count: Number of requested items, default 10
        :param offset: The offset for pagination, default 0
        :return: transfers
        """
        endpoint = '/private/get_deposits'
        params = f'currency={currency}&count={count}&offset={offset}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_get_withdrawals(self, currency, count=10, offset=0):
        """
        Retrieve the latest users deposits
        :param currency: BTC or ETH.
        :param count: Number of requested items, default 10
        :param offset: The offset for pagination, default 0
        :return: transfers
        """
        endpoint = '/private/get_withdrawals'
        params = f'currency={currency}&count={count}&offset={offset}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_get_transfers(self, currency, count=10, offset=0):
        """
        Adds new entry to address book of given type
        :param currency: BTC or ETH.
        :param count: Number of requested items, default 10
        :param offset: The offset for pagination, default 0
        :return: transfers
        """
        endpoint = '/private/get_transfers'
        params = f'currency={currency}&count={count}&offset={offset}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_user_order_history_by_currency(self, currency, kind, count=20, offset=0, include_old='true', include_unfilled='true'):
        """
        Retrieves history of orders that have been partially or fully filled.
        :param currency: BTC or ETH.
        :param kind: Instrument kind (option or future), if not provided instruments of all kinds are considered
        :param count: Number of requested items, default 20
        :param offset: The offset for pagination, default - 0
        :param include_old: Include trades older than a few recent days, default - false
        :param include_unfilled: Include in result fully unfilled closed orders, default - false
        :return: orders
        """
        endpoint = '/private/get_order_history_by_currency'
        params = f'currency={currency}&kind={kind}&count={count}&offset={offset}&include_old={include_old}&include_unfilled={include_unfilled}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_user_trades_by_currency(self, currency, kind, count=10, start_id=None, end_id=None, include_old='true', sorting='asc'):
        """
        Retrieve the latest user trades that have occurred for instruments in a specific currency symbol.
        :param currency: BTC or ETH.
        :param kind: Instrument kind (option or future), if not provided instruments of all kinds are considered
        :param count: Number of requested items, default 10
        :param start_id: The ID number of the first trade to be returned
        :param end_id: The ID number of the last trade to be returned
        :param include_old: Include trades older than a few recent days, default - false
        :param sorting: Direction of results sorting (default value means no sorting, results will be returned in order in which they left the database)
        :return: trades
        """
        endpoint = '/private/get_user_trades_by_currency'
        params = f'currency={currency}&kind={kind}&count={count}&include_old={include_old}&sorting={sorting}'
        if start_id is not None:
            params += f'&start_id={start_id}'
        if end_id is not None:
            params += f'&start_id={end_id}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_user_trades_by_order(self, order_id, sorting='asc'):
        """
        Retrieve the list of user trades that was created for given order
        :param order_id: The order id
        :param sorting: Direction of results sorting (default value means no sorting, results will be returned in order in which they left the database)
        :return: Given trade
        """
        endpoint = '/private/get_user_trades_by_order'
        params = f'order_id={order_id}&sorting={sorting}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_get_positions(self, currency, kind):
        """
        Retrieve user positions.
        :param currency: BTC or ETH.
        :param kind: future or option
        :return: positions
        """
        endpoint = '/private/get_positions'
        params = f'currency={currency}&kind={kind}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_get_settlement_by_currency(self, currency, type, count=10):
        """
        Retrieves settlement, delivery and bankruptcy events that have affected your account.
        :param currency: BTC or ETH.
        :param type: Settlement type. settlement, delivery or bankruptcy
        :param count: Number of requested items, default 10
        :return: settlements
        """
        endpoint = '/private/get_settlement_history_by_currency'
        params = f'currency={currency}&type={type}&count={count}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)

    def private_get_account_summary(self, currency, extended='false'):
        """
        Retrieves user account summary.
        :param currency: BTC or ETH.
        :param extended: Include additional fields
        :return: user account summary
        """
        endpoint = '/private/get_account_summary'
        params = f'currency={currency}&extended={extended}'
        return self.api_query(method='GET', params=params, endpoint=endpoint)