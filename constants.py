ACCOUNT_ID_1 = "101-003-25725464-001"
ACCOUNT_ID_2 = "101-003-25725464-002"
ACCOUNT_ID_3 = "101-003-25725464-003"
ACCOUNT_ID_4 = "101-003-25725464-004"
LIVE_ACCOUNT_ID = ""

PRACTICE_ACCESS_TOKEN = ""
LIVE_ACCESS_TOKEN = ""

LIVE_HEADERS = {"Authorization": f"Bearer {LIVE_ACCESS_TOKEN}", "Content-Type": "application/json"}
PRACTICE_HEADERS = {"Authorization": f"Bearer {PRACTICE_ACCESS_TOKEN}", "Content-Type": "application/json"}

LIVE_URL = "https://api-fxtrade.oanda.com/v3/accounts/{account_id}/"
PRACTICE_URL = "https://api-fxpractice.oanda.com/v3/accounts/{account_id}/"

CURRENCY_PAIRS = {"EUR": "EUR_SGD", "USD": "USD_SGD", "GBP": "GBP_SGD",
                  "NZD": "NZD_SGD", "AUD": "AUD_SGD", "CAD": "CAD_SGD"}

ORDER_DURATION_HOURS = 2
RISK_TOLERANCE = 0.02
