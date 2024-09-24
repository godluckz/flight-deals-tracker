import requests, json, sys
from os import path, environ
from flight_data import FlightData
from datetime import datetime, timedelta
from datetime_utils import ClassDateTimeUtils

W_TEQUILA_KIWI_QUERY_API_KEY  = environ.get("TEQUILA_KIWI_QUERY_API_KEY")
W_TEQUILA_KIWI_SEARCH_API_KEY  = environ.get("TEQUILA_KIWI_SEARCH_API_KEY")

W_TEQUILA_KIWI_BASE_URL = "https://api.tequila.kiwi.com"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.    
    def __init__(self) -> None:
        self.city_name = ""
        self.flight_deals = {}


    def get_city_aiport_code(self, p_city_name) -> str:
        # print(p_city_name)
        if not W_TEQUILA_KIWI_QUERY_API_KEY or not W_TEQUILA_KIWI_SEARCH_API_KEY:
            print("Flight Search-Code: Not all environment variables are loaded.")
            return None
        W_HEADERS = {"apikey": W_TEQUILA_KIWI_QUERY_API_KEY}
        W_TEQUILA_KIWI_URL = f"{W_TEQUILA_KIWI_BASE_URL}/locations/query"
        
        W_PARAMS = {
            "term"           : p_city_name,
            "location_types" : "city",
            "limit"          : 5
        }    
        
        w_response = requests.get(  url   = W_TEQUILA_KIWI_URL, 
                                    params= W_PARAMS,
                                    headers= W_HEADERS)
        w_response.raise_for_status()
        # print(w_response.text)
        try:
            w_location_data = w_response.json()["locations"][0] #only get first one
            # print(json.dumps(w_location_data , indent=4)) 
            w_code =  w_location_data["code"] 
        except Exception as e:
            print(f"Could not find airport code for: {p_city_name}")
            return None
        
        return w_code


    def search_flight_deals(self,
                            p_origin_city_iata      : str,
                            p_distination_city_iata : str,
                            p_date_from             : str,
                            p_date_to               : str,
                            p_nights_in_dst_from    : int = 7,
                            p_nights_in_dst_to      : int = 28,
                            p_currency              : str = "ZAR",                            
                            p_max_stopovers         : int = 0,
                            p_one_for_city          : int = 1 #cheapest flight 1 in a city
                            ) -> FlightData:
        w_gdate_util = ClassDateTimeUtils()
        if not W_TEQUILA_KIWI_QUERY_API_KEY or not W_TEQUILA_KIWI_SEARCH_API_KEY:
            print("Flight Search-Deals: Not all environment variables are loaded.")
            return None        
        W_SEARCH_HEADERS = {"apikey": W_TEQUILA_KIWI_SEARCH_API_KEY}        
        W_SEARCH_URL     = f"{W_TEQUILA_KIWI_BASE_URL}/v2/search"
        
        
        # print(w_fly_from_date,w_6months_date)        
        W_PARAMS = {
            "fly_from"          : p_origin_city_iata,
            "fly_to"            : p_distination_city_iata,
            "date_from"         : p_date_from,
            "date_to"           : p_date_to,
            "nights_in_dst_from": p_nights_in_dst_from,
            "nights_in_dst_to"  : p_nights_in_dst_to,
            "one_for_city"      : p_one_for_city,
            "curr"              : p_currency,   
            "max_stopovers"     : p_max_stopovers,
        }    
            
        w_response = requests.get(  url   = W_SEARCH_URL, 
                                    params= W_PARAMS,
                                    headers= W_SEARCH_HEADERS)
        w_response.raise_for_status()
        w_deals = w_response.json()        
        # print(json.dumps(w_deals , indent=4)) 
        try:
            w_flight_seach_data = w_deals["data"][0] #first result only
            w_flight_route      = w_flight_seach_data["route"]
            # print(json.dumps(w_flight_route , indent=4)) 
        except Exception as e:
            # print("No flights found.")
            return None
        
        w_out_date    = w_gdate_util.get_date_and_time_local(w_flight_route[0]["local_departure"])[0]
        w_return_date = w_gdate_util.get_date_and_time_local(w_flight_route[1]["local_departure"])[0]
        # print(w_out_date, w_return_date)
        
        w_flight_data = FlightData( p_origin_city         = w_flight_route[0]["cityFrom"], 
                                    p_origin_airport      = w_flight_route[0]["flyFrom"], 
                                    p_destination_city    = w_flight_route[0]["cityTo"], 
                                    p_destination_airport = w_flight_route[0]["flyTo"], 
                                    p_out_date            = w_out_date,  
                                    p_return_date         = w_return_date, 
                                    p_price               = w_flight_seach_data["price"])
        print(f"{w_flight_data.destination_city}: R{w_flight_data.price:,}")
        return w_flight_data
            

def main() -> None:
    W_TRAVEL_ORIGIN : tuple = ("Johannesburg","JNB", "ZAR", 1)        
    W_TRAVEL_ORIGIN_CITY      : str = W_TRAVEL_ORIGIN[0]    
    W_TRAVEL_ORIGIN_IATA_CODE : str = W_TRAVEL_ORIGIN[1]
    W_CURRENCY                : str = W_TRAVEL_ORIGIN[2]
    W_MAX_STOPOVER            : int = W_TRAVEL_ORIGIN[3]
    W_DAYS_FROM_TODAY_FROM    : int = 7
    W_DAYS_FROM_TODAY_TO      : int = 1*30 # 6 months    
    # print(W_TRAVEL_ORIGIN_CITY, W_TRAVEL_ORIGIN_IATA_CODE) 
    
    from data_manager import DataManager
    W_FLIGHT_DATA_MANAGER   = DataManager()    
    w_flight_cities = W_FLIGHT_DATA_MANAGER.get_flight_destination_data()    
    if w_flight_cities == None or not w_flight_cities:
        print("Main:: Something is fishy - check google sheets and sheety to make sure all is well and try again. Thank you.")
        return
    
    # print(json.dumps(w_flight_cities , indent=4))                

    for row in w_flight_cities:        
        w_city = row["city"]                
        if row["iataCode"] == "":            
            W_FLIGHT_SEARCH = FlightSearch()
            w_city_code = W_FLIGHT_SEARCH.get_city_aiport_code(w_city)  #using Tequila                        
            row["iataCode"] = w_city_code  #will chage the original values because of reference point
    
    W_FLIGHT_DATA_MANAGER.detindation_data = w_flight_cities    
    
    W_FLIGHT_DATA_MANAGER.update_destination_aiport_codes()
    
    #------------------------#
    #----search for deals----#
    #------------------------#    
    for w_destination in W_FLIGHT_DATA_MANAGER.detindation_data:
        w_destination_city = w_destination["city"]
        w_destination_city_iata_code = w_destination["iataCode"]
        # print(w_destination_city)
            
        
        # direct flights
        # leave anytime between tomorrow and in 6 months (6x30days) time. 
        # round trips that return between 7 and 28 days in length. 
        # The currency of the price we get back should be in ZAR.
        
                
        W_FLIGHT_SEARCH        = FlightSearch()
        w_today                = datetime.now()        
        w_date_from_today_from = w_today + timedelta(W_DAYS_FROM_TODAY_FROM) 
        w_date_from_today_to   = w_today + timedelta(W_DAYS_FROM_TODAY_TO)        
        
        w_departure_date_from = w_date_from_today_from.strftime("%d/%m/%Y")        
        w_departure_date_to   = w_date_from_today_to.strftime("%d/%m/%Y")      
                
        w_flight_deals: FlightData = W_FLIGHT_SEARCH.search_flight_deals(   p_origin_city_iata      = W_TRAVEL_ORIGIN_IATA_CODE,
                                                                            p_distination_city_iata = w_destination_city_iata_code,
                                                                            p_date_from             = w_departure_date_from,
                                                                            p_date_to               = w_departure_date_to,
                                                                            p_currency              = W_CURRENCY,
                                                                            p_max_stopovers         = W_MAX_STOPOVER,                                                                            
                                                                            )    #uses tequila
        
        if w_flight_deals == None:
            print(f":( No flights from {W_TRAVEL_ORIGIN_CITY}-{W_TRAVEL_ORIGIN_IATA_CODE} to {w_destination_city}-{w_destination_city} for the given dates")       
        else:
            print(f"""Flights from {W_TRAVEL_ORIGIN_CITY}-{W_TRAVEL_ORIGIN_IATA_CODE} to {w_destination_city}-{w_destination_city} will cost : {w_flight_deals.price}
                   \nDeparture: {w_flight_deals.out_date}"
                   \nReturn: {w_flight_deals.return_date}"
                   """)       
        print("---------------------------")
        

if __name__ == "__main__":
    main()

    print("***************************")
    print("!!Tequila Unit test - Procesing completed!!")
    print("Thank You. Bye")        
    print("***************************")         