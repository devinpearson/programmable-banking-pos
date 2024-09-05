import requests

class Issuer():
    def __init__(self, host):
        self.host = host

    def getDetails(self, id):
            # The API endpoint to communicate with
            url = self.host + "/terminals/" + str(id)

            # A GET request to tthe API
            response = requests.get(url)
            if response.status_code == 200:
                print('Success!')
                response_json = response.json()
                # global currency
                currency = response_json["symbol"]
                return currency
                print(response_json)
            elif response.status_code == 404:
                print('Terminal not registered. Terminal: ' + str(id))
                sys.exit(1)
            else:
                print('Something went wrong ' + str(response.status_code))

    def postTransaction(self, amount, value, id):
        print(value)
        new_data = {
            "centsAmount": str(amount)+'00',
            "card": str(value),
            "terminalId": str(id)
        }

        # The API endpoint to communicate with
        url_post = self.host + "/terminals/" + str(id) + "/transactions"

        # A POST request to tthe API
        response = requests.post(url_post, json=new_data)
        if response.status_code == 200:
            print('Success!')
            # Print the response
            response_json = response.json()
            print(response_json)
            return response_json["result"]
        else:
            print('Something went wrong ' + str(response.status_code))
            return False