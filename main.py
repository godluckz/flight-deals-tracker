#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import requests, json
from os import environ
from class_flight_search_tequila import FlightSearch
from data_manager import DataManager
from datetime import datetime, timedelta
from flight_data import FlightData

W_FLIGHT_DATA_MANAGER   = DataManager()   

W_TRAVEL_ORIGIN : tuple = ("Johannesburg","JNB", "ZAR", 1)
# W_TRAVEL_ORIGIN : tuple = ("London","LON", "GBP", 0)
W_DAYS_FROM_TODAY_FROM : int = 7
W_DAYS_FROM_TODAY_TO   : int = 1*30 # 6 months

W_TRAVEL_ORIGIN_CITY      : str = None
W_TRAVEL_ORIGIN_IATA_CODE : str = None
W_CURRENCY                : str = None
W_MAX_STOPOVER            : int = None

def set_origin_travel_details() -> None:   
    """
    Set travel Origin details, can be set to be user input
    """      
    global W_TRAVEL_ORIGIN_CITY,W_TRAVEL_ORIGIN_IATA_CODE,W_CURRENCY,W_MAX_STOPOVER
 
    W_TRAVEL_ORIGIN_CITY      = W_TRAVEL_ORIGIN[0]    
    W_TRAVEL_ORIGIN_IATA_CODE = W_TRAVEL_ORIGIN[1]
    W_CURRENCY                = W_TRAVEL_ORIGIN[2]
    W_MAX_STOPOVER            = W_TRAVEL_ORIGIN[3]
    # print(W_TRAVEL_ORIGIN_CITY, W_TRAVEL_ORIGIN_IATA_CODE) 



def load_flight_cities() -> None: 
    """
    Get destination options from Sheety or local file if exists.
    Update IATA airport codes for the destinations
    """      
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



def search_for_flight_deals() -> None:
    """
    search for deals
    """    
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



def main() -> None:      

    set_origin_travel_details()
    
    load_flight_cities()
    
    search_for_flight_deals()


    print("***************************")
    print("!!Procesing completed!!")
    print("Thank You. Bye")        
    print("***************************") 

if __name__ == "__main__":    
    main()