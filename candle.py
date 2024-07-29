import constants
import requests
from datetime import datetime, timedelta
import json


def fetch_candle_data(start_date, end_date, timeframe, instrument):
    # Define the date range
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    url = f"https://api-fxtrade.oanda.com/v3/instruments/{instrument}/candles"

    # Function to fetch data
    def fetch_oanda_data(start, end):
        params = {
            "granularity": timeframe,
            "price": "M",
            "from": start.strftime("%Y-%m-%dT%H:%M:%S") + "Z",
            "to": end.strftime("%Y-%m-%dT%H:%M:%S") + "Z",
            "alignmentTimezone": "UTC"
        }
        response = requests.get(url, headers=constants.LIVE_HEADERS, params=params)
        if response.status_code == 200:
            return response.json()["candles"]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    # Fetch data in batches due to rate limit
    current_date = start_date
    data = []

    while current_date < end_date:
        next_date = min(current_date + timedelta(days=5), end_date)  # Fetch 5 days at a time
        data.extend(fetch_oanda_data(current_date, next_date))
        current_date = next_date

    # Save the collected data to a JSON file
    with open("candle_data.json", 'w') as file:
        json.dump(data, file, indent=2)

    return json.dumps(data, indent=2)


def fetch_current_closing_price(timeframe, instrument):
    time_now = datetime.now()
    target_time = time_now.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
    print(target_time)
    target_time = "2023-05-25T03:30:00Z"
    url = "https://api-fxpractice.oanda.com/v3/accounts/{account_id}/instruments/{instrument}/candles"

    # Set the parameters for the API request
    params = {
        "granularity": timeframe,
        "price": "M",
        "from": target_time,
        "count": 1,  # Fetch only one candle
        "alignmentTimezone": "UTC",  # Set the alignment timezone to UTC
    }

    response = requests.get(url.format(account_id=constants.ACCOUNT_ID, instrument=instrument),
                            headers=constants.HEADERS, params=params)

    # Check the response status code
    if response.status_code == 200:
        # Retrieve the candle data from the response
        candle = response.json()["candles"][0]
        print(candle)
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

        print(1000 / close_price)
    else:
        # Request unsuccessful, display the error message
        print("Error:", response.json()["errorMessage"])
