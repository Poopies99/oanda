import json
import constants
import oanda


def handler(event, context):
    try:
        # Initiate Client Class
        client = oanda.Oanda(constants.LIVE_ACCOUNT_ID)

        details = json.loads(event['body'])

        if 'SAR' in details:
            price = details['Price']
            instrument = details['Instrument'][:3] + '_' + details['Instrument'][3:]
            """
            if details['SAR'] == 'Long':

            elif details['SAR'] == 'Short':

            else:
                print("Invalid SAR value")
            """
        else:
            # Parse JSON Values
            instrument = details['Instrument'][:3] + '_' + details['Instrument'][3:]
            price = details['Price']
            stop_loss = details['Stop_Loss']
            take_profit = details['Take_Profit']

            if client.check_order_and_positions(instrument):
                client.create_limit_order(instrument, price, take_profit, stop_loss)
            else:
                print("There is an order/open position for the following instrument")

        return details
    except Exception as e:
        print('Something is not right my guy', e)

    return event

handler()
