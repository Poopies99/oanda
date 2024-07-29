import requests
import constants

def fetch_canceled_order(order_id):
    url = f"https://api-fxpractice.oanda.com/v3/accounts/{constants.ACCOUNT_ID}/orders/{order_id}"

    response = requests.get(url, headers=constants.HEADERS)

    # Check the response status code
    if response.status_code == 200:
        # Order details successfully retrieved
        order_details = response.json()['order']
        return order_details
        if order_details["state"] == "CANCELLED":
            return order_details
        else:
            print("Error: The specified order is not canceled.")
    else:
        # Request unsuccessful, display the error message
        print("Error:", response.json()["errorMessage"])

# Usage example:
canceled_order_id = "338"  # Replace with the ID of the canceled order
order_details = fetch_canceled_order(canceled_order_id)
print(order_details)
