from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

my_data_manager = DataManager()
sheet_data = my_data_manager.pass_data_over()

my_flight_search = FlightSearch()
my_notification_manager = NotificationManager()

for city_data in sheet_data:
    # access each element of the dictionary
    city_name = city_data['city']
    iata_code = city_data['iataCode']
    lowest_price = city_data['lowestPrice']
    city_id = city_data['id']
    dest_code = my_flight_search.get_dest_code(city_name)
    # this gets the iata code for the destination based on the city name, using the tequila.kiwi api.
    flight_data_object = my_flight_search.search_for_flights(dest_code)
    # this gets the cheapest flight from london based on the destination iata code using the tequila.kiwi api.
    if iata_code == "":
        my_data_manager.populate_IATA_code(iataCode=dest_code, id=city_id)
        #my flight tracker sheet starts out with a non-populated iataCode column. This populates the column.
    if lowest_price > flight_data_object.price:
        my_data_manager.populate_price(price=flight_data_object.price, id=city_id)
        # if the current price is lower, populate the price column of the lower price.
        print("found a deal! sending email!")
        my_notification_manager.send_email(flight_data_object.price,
                                           flight_data_object.origin_city,
                                           flight_data_object.origin_airport,
                                           flight_data_object.destination_city,
                                           flight_data_object.destination_airport,
                                           flight_data_object.out_date,
                                           flight_data_object.return_date)
    print(f"{city_name}: {flight_data_object.price}")


