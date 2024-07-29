import requests
import json
import constants
import datetime


class Oanda:
    def __init__(self, account_id):
        self.account_id = account_id
        self.account = self.fetch_account_details()
        # self.account_balance = float(self.account["balance"])
        self.account_balance = 2500 + float(self.account['pl'])
        print(self.account_balance)

    def fetch_account_details(self):
        url = "https://api-fxtrade.oanda.com/v3/accounts/{account_id}/summary"

        response = requests.get(url.format(account_id=self.account_id), headers=constants.LIVE_HEADERS)

        # Check the response status code
        if response.status_code == 200:
            # Request successful, retrieve the account balance
            return response.json()["account"]
        else:
            # Request unsuccessful, display the error message
            print("Error:", response.json()["errorMessage"])

    def create_market_order(self, instrument, quantity, take_profit=None, stop_loss=None):
        payload = {
            "order": {
                "instrument": instrument,
                "units": quantity,
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }

        if take_profit:
            payload["order"]["takeProfitOnFill"] = {"price": self.refine_price(take_profit)}

        if stop_loss:
            payload["order"]["stopLossOnFill"] = {"price": self.refine_price(stop_loss)}

        url = constants.LIVE_URL

        response = requests.post(url.format(account_id=self.account_id), headers=constants.LIVE_HEADERS,
                                 data=json.dumps(payload))

        # Check the response status code
        if response.status_code == 201:
            # Order successfully placed
            print("Order placed successfully!")
        else:
            # Request unsuccessful, display the error message
            print("Error:", response.json()["errorMessage"])

    def create_limit_order(self, instrument, price, take_profit=None, stop_loss=None):
        # Calculate quantity
        quantity = self.calculate_quantity(price, stop_loss, instrument)

        # Calculate the expiry datetime
        current_time = datetime.datetime.utcnow()
        expiry_time = current_time + datetime.timedelta(hours=constants.ORDER_DURATION_HOURS)

        # Convert expiry_time to ISO 8601 format
        expiry_time_iso = expiry_time.isoformat() + "Z"

        payload = {
            "order": {
                "instrument": instrument,
                "units": int(quantity),
                "price": self.refine_price(price),
                "type": "LIMIT",
                "positionFill": "DEFAULT",
                "timeInForce": "GTD",
                "gtdTime": expiry_time_iso
            }
        }

        if take_profit:
            payload["order"]["takeProfitOnFill"] = {"price": self.refine_price(take_profit)}

        if stop_loss:
            payload["order"]["stopLossOnFill"] = {"price": self.refine_price(stop_loss)}

        url = constants.LIVE_URL

        response = requests.post(url.format(account_id=self.account_id), headers=constants.LIVE_HEADERS,
                                 data=json.dumps(payload))

        # Check the response status code
        if response.status_code == 201:
            # Order successfully placed
            print("Order placed successfully!")
            print(response.json())
        else:
            # Request unsuccessful, display the error message
            print("Error:", response.json()["errorMessage"])

    def cancel_all_orders(self):
        # Orders do not include Take Profit and Stop Loss
        url = f"https://api-fxtrade.oanda.com/v3/accounts/{self.account_id}/orders"

        response = requests.get(url, headers=constants.LIVE_HEADERS)

        # Check the response status code
        if response.status_code == 200:
            orders = response.json()["orders"]
            if orders:
                for order in orders:
                    order_id = order["id"]
                    order_type = order["type"]
                    if order_type != "STOP_LOSS" and order_type != "TAKE_PROFIT":
                        cancel_url = f"{url}/{order_id}/cancel"
                        cancel_response = requests.put(cancel_url, headers=constants.LIVE_HEADERS)
                        if cancel_response.status_code == 200:
                            print(f"Order {order_id} canceled successfully!")
                        else:
                            print(f"Error canceling order {order_id}: {cancel_response.json()['errorMessage']}")
            else:
                print("No open orders to cancel.")
        else:
            print("Error:", response.json()["errorMessage"])

    def fetch_open_positions(self, instrument):
        url = "https://api-fxtrade.oanda.com/v3/accounts/{account_id}/openPositions"

        params = {
            "instrument": instrument
        }

        response = requests.get(url.format(account_id=self.account_id), headers=constants.LIVE_HEADERS, params=params)

        # Check the response status code
        if response.status_code == 200:
            # Request successful, retrieve the open positions
            return response.json()['positions']
        else:
            # Request unsuccessful, display the error message
            print("Error:", response.json()["errorMessage"])

    def fetch_orders(self, instrument):
        url = "https://api-fxtrade.oanda.com/v3/accounts/{account_id}/orders"

        params = {
            "instrument": instrument,
            "state": "PENDING"
        }

        response = requests.get(url.format(account_id=self.account_id), headers=constants.LIVE_HEADERS, params=params)

        # Check the response status code
        if response.status_code == 200:
            # Request successful, retrieve all orders
            return response.json()["orders"]
        else:
            # Request unsuccessful, display the error message
            print("Error:", response.json()["errorMessage"])

    def calculate_quantity(self, entry_price, stop_loss_price, currency_pair):
        account_balance_base_currency = self.get_base_currency_balance(self.account_balance, currency_pair)

        risk_amount = constants.RISK_TOLERANCE * account_balance_base_currency
        return risk_amount / (1 - (stop_loss_price / entry_price))

    def refine_price(self, number):
        return format(number, ".6g")

    def fetch_candle_data(self, timeframe, instrument):
        url = "https://api-fxtrade.oanda.com/v3/accounts/{account_id}/instruments/{instrument}/candles"

        # Set the parameters for the API request
        params = {
            "granularity": timeframe,
            "price": "M",
            "count": 1,  # Fetch only the most recent candle
            "alignmentTimezone": "UTC",  # Set the alignment timezone to UTC
        }

        response = requests.get(url.format(account_id=self.account_id, instrument=instrument),
                                headers=constants.LIVE_HEADERS, params=params)

        # Check the response status code
        if response.status_code == 200:
            # Retrieve the candle data from the response
            candle = response.json()["candles"][0]

            # Extract the open, close, high, and low prices
            open_price = float(candle["mid"]["o"])
            close_price = float(candle["mid"]["c"])
            high_price = float(candle["mid"]["h"])
            low_price = float(candle["mid"]["l"])

            # Print the retrieved prices
            print(f"Open: {open_price}")
            print(f"Close: {close_price}")
            print(f"High: {high_price}")
            print(f"Low: {low_price}")
        else:
            # Request unsuccessful, display the error message
            print("Error:", response.json()["errorMessage"])

    def get_base_currency_balance(self, sgd_balance, currency_pair):
        base_currency = currency_pair[:3]

        exchange_currency_pair = constants.CURRENCY_PAIRS[base_currency]

        url = "https://api-fxtrade.oanda.com/v3/accounts/{account_id}/instruments/{instrument}/candles"

        params = {
            "granularity": "M1",
            "count": 1
        }

        response = requests.get(url.format(account_id=self.account_id, instrument=exchange_currency_pair),
                                headers=constants.LIVE_HEADERS, params=params)

        if response.status_code == 200:
            data = response.json()

            if "candles" in data:
                candles = data["candles"]
                if len(candles) > 0:
                    last_closing_price = candles[-1]["mid"]["c"]
                    return sgd_balance / float(last_closing_price)
        else:
            # Request unsuccessful, display the error message
            print("Error:", response.json()["errorMessage"])

    def check_order_and_positions(self, instrument):
        print(len(self.fetch_orders(instrument)))
        print(len(self.fetch_open_positions(instrument)))
        return len(self.fetch_orders(instrument)) == 0 and len(self.fetch_open_positions(instrument)) == 0


o = Oanda(constants.LIVE_ACCOUNT_ID)
print(o.check_order_and_positions("EUR_JPY"))