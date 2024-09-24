import requests, json, sys
from os import path, environ
from flight_data import FlightData
from datetime import datetime, timedelta
from datetime_utils import ClassDateTimeUtils

SKYSCANNER_HOST        = "skyscanner80.p.rapidapi.com"
SKYSCANNER_BASE_URL    = f"https://{SKYSCANNER_HOST}"
SKYSCANNER_API_URL     = f"{SKYSCANNER_BASE_URL}/api/v1"
SKYSCANNER_FLIGHTS_URL = f"{SKYSCANNER_API_URL}/flights"
SKYSCANNER_API_KEY     = environ.get("SKYSCANNER_API_KEY")

class FlightSearch:
    def __init__(self) -> None:
        pass

    def search_airports(self, p_query):

        url = f"{SKYSCANNER_FLIGHTS_URL}/auto-complete"

        querystring = {"query":p_query,
                    "market":"ZA",
                    "locale":"en-GB"}

        headers = {
            "X-RapidAPI-Key": SKYSCANNER_API_KEY,
            "X-RapidAPI-Host": SKYSCANNER_HOST
        }

        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
                
        return response.json()

    def search_flights(self, 
                       p_origin, 
                       p_destination,
                       p_depature_date,
                       p_return_date) -> None:
        
        w_frm_airport = self.search_airports(p_origin)
        # print(json.dumps(w_jhb_airport , indent=4))     
        w_from_airport_name = w_frm_airport['data'][0]['presentation']['title']
        w_from_airport_id   = w_frm_airport['data'][0]['id']
        # print(f"{w_from_airport_name}: {w_from_airport_id}")    
        
        w_to_airport = self.search_airports(p_destination)    
        # print(json.dumps(w_dar_airport , indent=4)) 
        w_to_aiport_name = w_to_airport['data'][0]['presentation']['title']
        w_to_aiport_id   = w_to_airport['data'][0]['id']
        # print(f"{w_to_aiport_name}: {w_to_aiport_id}")    
        
        url = f"{SKYSCANNER_FLIGHTS_URL}/search-roundtrip"

        print(f"Will search for the trip\n From: {w_from_airport_name}\n To: {w_to_aiport_name}\nDeparture: {p_depature_date}\nReturn: {p_return_date}")
        querystring = {"fromId"     : w_from_airport_id,
                    "toId"       : w_to_aiport_id,
                    "departDate" : p_depature_date,
                    "returnDate" : p_return_date,
                    "adults"     : "1",
                    "currency"   : "ZAR",
                    "market"     : "ZA",
                    "locale"     : "en-GB"}

        headers = {
            "X-RapidAPI-Key": SKYSCANNER_API_KEY,
            "X-RapidAPI-Host": SKYSCANNER_HOST
        }

        response = requests.get(url, headers=headers, params=querystring)

        print(json.dumps(response.json() , indent=4))     
        
            
    def get_skyscanner_config(self):
        url = f"{SKYSCANNER_API_URL}/get-config"

        headers = {
            "X-RapidAPI-Key": SKYSCANNER_API_KEY,
            "X-RapidAPI-Host": SKYSCANNER_HOST
        }

        response = requests.get(url, headers=headers)
        print(json.dumps(response.json() , indent=4)) 



def main() -> None:
    w_today               = datetime.now()      

    W_TRIP_DAYS        = timedelta(days=30)
    W_DAYS_FROM_TODAY  = timedelta(days=7)            

    w_departure_date = w_today + W_DAYS_FROM_TODAY    
    w_return_date    = w_departure_date + W_TRIP_DAYS
    
    w_departure_date = w_departure_date.strftime("%Y-%m-%d")
    w_return_date    = w_return_date.strftime("%Y-%m-%d")    

    w_origin_airport      = "Johannesburg O.R. Tambo"
    w_destination_airport = "Dar es Salaam DAR"     

    W_FLIGHT_SEARCH = FlightSearch()
    # W_FLIGHT_SEARCH.get_skyscanner_config() #Gives you country details.
    W_FLIGHT_SEARCH.search_flights(p_origin        = w_origin_airport,
                                   p_destination   = w_destination_airport,
                                   p_depature_date = w_departure_date,
                                   p_return_date   = w_return_date)
        
    print("---------------------------")



if __name__ == "__main__":
    main()
    print("***************************")
    print("!!Skyscanner Unit test - Procesing completed!!")
    print("Thank You. Bye")        
    print("***************************")     
        