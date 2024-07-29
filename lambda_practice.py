import json
import requests
import constants


def get_account_id(strategy):
    if strategy == 'ASK Strategy 1':
        return constants.ACCOUNT_ID_2
    elif strategy == 'ASK Strategy 2':
        return constants.ACCOUNT_ID_3
    elif strategy == 'AST Strategy 1':
        return constants.ACCOUNT_ID_4
    else:
        return constants.ACCOUNT_ID_1


# def handler(event, context):
#     try:
#         details = json.loads(event['body'])
#         client = oanda.Oanda(constants.ACCOUNT_ID_1)
#
#         if 'SAR' in details:
#             price = details['Price']
#             instrument = details['Instrument'][:3] + '_' + details['Instrument'][3:]
#
#             if details['SAR'] == 'Long':
#
#
#             elif details['SAR'] == 'Short':
#                 # Todo
#
#             else:
#                 print("Invalid SAR value")
#
#         else:
#             # Parse JSON Values
#             instrument = details['Instrument'][:3] + '_' + details['Instrument'][3:]
#             price = details['Price']
#             stop_loss = details['Stop_Loss']
#             take_profit = details['Take_Profit']
#             account_id = constants.ACCOUNT_ID
#
#             # Initiate Client Class
#             # client = oanda.Oanda(account_id)
#
#             if client.check_order_and_positions(instrument):
#                 client.create_limit_order(instrument, price, take_profit, stop_loss)
#             else:
#                 print("There is an order/open position for the following instrument")
#
#         return details
#     except Exceptiona as e:
#         print('Something is not right my guy', e)
#
#     return event

def handler():

    # Your OANDA API key
    api_key = constants.PRACTICE_ACCESS_TOKEN
    # OANDA Account ID
    account_id = constants.ACCOUNT_ID_1

    # Define the instrument and time frame
    instrument = 'EUR_JPY'
    granularity = 'M15'  # 15-minute candles

    # Define the date range
    start_date = datetime.strptime('2024-06-26', '%Y-%m-%d')
    end_date = datetime.strptime('2024-07-17', '%Y-%m-%d')

    # OANDA API endpoint for fetching historical data
    url = f"https://api-fxtrade.oanda.com/v3/instruments/{instrument}/candles"

    # Function to fetch data
    def fetch_oanda_data(start, end):
        headers = {
            'Authorization': f'Bearer {api_key}'
        }

        params = {
            'from': start.isoformat(),
            'to': end.isoformat(),
            'granularity': granularity,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    # Fetch data in batches (OANDA limits the amount of data per request)
    current_date = start_date
    data = []

    while current_date < end_date:
        next_date = min(current_date + timedelta(days=5), end_date)  # Fetch 5 days at a time
        result = fetch_oanda_data(current_date, next_date)
        if result:
            data.extend(result['candles'])
        current_date = next_date

    # Print the collected data
    print(json.dumps(data, indent=2))

    """
    try:
        # details = json.loads(event['body'])
        details = {'Instrument': 'EURSGD', 'SAR': 'Long', 'Price': 1.476}
        client = oanda.Oanda(constants.ACCOUNT_ID_1, constants.PRACTICE_URL, constants.PRACTICE_HEADERS)

        if 'SAR' in details:
            price = details['Price']
            instrument = details['Instrument'][:3] + '_' + details['Instrument'][3:]
            positions = client.fetch_open_positions(instrument)

            if details['SAR'] == 'Long':
                if len(positions) != 0:
                    for position in positions:
                        # If there exists a short position for the instrument
                        if position['instrument'] == instrument and abs(int(position['short']['units'])) > 0:
                            # client.close_trade(position['short']['tradeIDs'][0]) # Should only have one open position everytime
                            client.create_closing_limit_order(instrument, price, int(position['short']['units']))
                            print("Following Position has been closed", position['short'])
                            break
                else:
                    print("No Open Positions to Close")

            elif details['SAR'] == 'Short':
                if len(positions) != 0:
                    for position in positions:
                        # If there exists a long position for the instrument
                        if position['instrument'] == instrument and abs(int(position['long']['units'])) > 0:
                            # client.close_trade(position['long']['tradeIDs'][0])
                            client.create_closing_limit_order(instrument, price, -int(position['long']['units']))
                            print("Following Position has been closed", position['long'])
                            break
                else:
                    print("No Open Positions to Close")

            else:
                print("Invalid SAR value")

        else:
            # Parse JSON Values
            instrument = details['Instrument'][:3] + '_' + details['Instrument'][3:]
            price = details['Price']
            stop_loss = details['Stop_Loss']
            take_profit = details['Take_Profit']
            account_id = constants.ACCOUNT_ID

            # Initiate Client Class
            # client = oanda.Oanda(account_id)

            if client.check_order_and_positions(instrument):
                client.create_limit_order(instrument, price, take_profit, stop_loss)
            else:
                print("There is an order/open position for the following instrument")

        return details
    except Exception as e:
        print('Something is not right my guy', e)

    return event
    """
handler()
