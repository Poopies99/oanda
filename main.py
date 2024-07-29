import candle


def main():
    start_date = '2023-06-26'
    end_date = '2023-07-17'
    timeframe = 'M15' # 15 Minutes CandleStick
    instrument = 'EUR_JPY'

    candle_data = candle.fetch_candle_data(start_date, end_date, timeframe, instrument)
    print(candle_data)


main()
