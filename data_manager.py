import json
import requests
import os

BEARER_TOKEN = os.environ['BEARER_TOKEN']
SHEETY_ENDPOINT = os.environ['SHEETY_ENDPOINT']


class DataManager:
    def __init__(self):
        self.BEARER_TOKEN = os.environ['BEARER_TOKEN']
        self.sheety_endpoint = f"{SHEETY_ENDPOINT}"
        self.headers = {
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }

    def pass_data_over(self):
        """returns the spreadsheet data"""
        response = requests.get(url=self.sheety_endpoint, headers=self.headers)
        sheety_json = json.loads(response.text)
        sheety_json_prices = sheety_json['prices']
        print(os.environ['SHEETY_ENDPOINT'])
        return sheety_json_prices

    def populate_IATA_code(self, iataCode, id):
        """pupulate the iata column of the spreadsheet"""
        data = {
            "price": {
                "iataCode": iataCode,
            }
        }
        response_put = requests.put(url=f"{self.sheety_endpoint}/{id}", json=data, headers=self.headers)

    def populate_price(self, price, id):
        """Populates the spreadsheet with new lower price"""
        data = {
            "price": {
                "lowestPrice": price,
            }
        }
        response_put = requests.put(url=f"{self.sheety_endpoint}/{id}", json=data, headers=self.headers)
