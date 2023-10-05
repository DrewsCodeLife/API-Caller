from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

client = CryptoHistoricalDataClient()

start_date = datetime(2022, 9, 1).isoformat() + "Z"
end_date = datetime(2022, 9, 7).isoformat() + "Z"

request_params = CryptoBarsRequest(
                        symbol_or_symbols = ["BTC/USD"],
                        timeframe = TimeFrame.Day,
                        start = start_date,
                        end = end_date
                        )

btc_bars = client.get_crypto_bars(request_params)
btc_bars.df