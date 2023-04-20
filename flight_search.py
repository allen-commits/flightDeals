import requests
import json
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flight_data import FlightData

API_KEY = os.environ['apikey']
URL_QUERY = "https://api.tequila.kiwi.com/locations/query"
URL_SEARCH = "https://api.tequila.kiwi.com/v2/search"


class FlightSearch:

    def get_dest_code(self, city_name):
        """Returns the iata code of city using the tequila.kiwi api"""
        json_data = {
            "term": city_name,
            "location_types": "city",
            "limit": "1",
            "active_only": "true"
        }
        headers = {
            "apikey": API_KEY
        }
        response = requests.get(url=URL_QUERY, params=json_data, headers=headers)
        flight_search_json = json.loads(response.text)
        iata_code = flight_search_json['locations'][0]['code']
        return iata_code

    def search_for_flights(self, iata_code):
        """This searches the tequila.kiwi api for the cheapest flight between now and 6 months forward, then returns the
         values in a FlightData object"""
        tomorrow = datetime.now() + timedelta(1)
        tomorrow_formatted = tomorrow.strftime("%d/%m/%Y")

        in_six_months = datetime.now() + relativedelta(months=+6)
        in_six_months_formatted = in_six_months.strftime("%d/%m/%Y")
        json_data = {
            "fly_from": "LON",
            "fly_to": iata_code,
            "date_from": tomorrow_formatted,
            "date_to": in_six_months_formatted,
            "nights_in_dst_from": "6",
            "nights_in_dst_to": "27",
            "flight_type": "round",
            "curr": "GBP",
            "max_stopovers": "0"
        }
        headers = {
            "apikey": API_KEY
        }
        response = requests.get(url=URL_SEARCH, params=json_data, headers=headers)

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"Sorry! No flights found for {iata_code}")
            return None
        flight_search_json = json.loads(response.text)

        api_outbound_date = flight_search_json['data'][0]['route'][0]['local_departure']
        api_outbound_date = datetime.fromisoformat(api_outbound_date[:-1])
        api_outbound_date = api_outbound_date.strftime("%m/%d/%Y")

        api_inbound_date = flight_search_json['data'][1]['route'][1]['local_departure']
        api_inbound_date = datetime.fromisoformat(api_inbound_date[:-1])
        api_inbound_date = api_inbound_date.strftime("%m/%d/%Y")

        flight_data = FlightData(
            price=flight_search_json['data'][0]['price'],
            origin_city=flight_search_json['data'][0]['cityFrom'],
            origin_airport=flight_search_json['data'][0]['flyFrom'],
            destination_city=flight_search_json['data'][0]['cityTo'],
            destination_airport=flight_search_json['data'][0]['flyTo'],
            out_date=api_outbound_date,
            return_date=api_inbound_date
        )
        return flight_data


