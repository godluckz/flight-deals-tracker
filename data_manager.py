import requests, json
from os import path, environ
from class_flight_search_tequila import FlightSearch

W_SHEETY_KEY          = environ.get("SHEETY_KEY")
W_SHEETY_BEARER_AUTH  = environ.get("SHEETY_BEARER_AUTH")
W_SHEETY_URL          = f"https://api.sheety.co/{W_SHEETY_KEY}/flightDeals/prices"
W_SHEETY_HEADERS      = {"Authorization": f"Bearer {W_SHEETY_BEARER_AUTH}"}


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self) -> None:
        self.detindation_data = {}
    

    def update_destination_aiport_codes(self) -> None:        
        # print(json.dumps(self.detindation_data , indent=4)) 
        if not W_SHEETY_KEY or not W_SHEETY_BEARER_AUTH:
            print("Data Manager: Not all environment variables are loaded.")
            return 
        for city in self.detindation_data:
            # print(city)
            w_new_data = {
                "price":{
                        "iataCode": city["iataCode"]
                    }
            }
            try:
                W_RESPONSE = requests.put(  url=f"{W_SHEETY_URL}/{city['id']}", 
                                            json=w_new_data,
                                            headers=W_SHEETY_HEADERS,
                                            )
                W_RESPONSE.raise_for_status()
            except Exception as e:
                print(f"Fail to update iata code for city: {city['city']}, msg: {e}")
            # print(W_RESPONSE.text)
            # self.detindation_data = W_RESPONSE.json()["prices"]        
            
    
    def get_flight_destination_data(self) -> list:                    
        def get_destination_data_local() -> json:
            import pandas
                        
            W_CURR_DIR = path.dirname(__file__)                                    
            W_FLIGHT_DEALS_PATH = f"{W_CURR_DIR}/data/Flight Deals - prices.csv"
            w_csv_results : pandas.DataFrame = pandas.read_csv(W_FLIGHT_DEALS_PATH)
            # print(w_csv_results)
            
            w_local_data_return = []
            w_id : int = 0
            for key, cities in w_csv_results.iterrows():
                w_id += 1
                # print(cities["City"])
                w_local_data = {}
                w_local_data["id"]       = w_id
                w_local_data["city"]     = cities["City"]
                w_local_data["iataCode"] = cities["IATA Code"]                                              
                w_local_data_return.append(w_local_data)
            # print(w_local_data_return)  
            return w_local_data_return
                
        try:
            if not W_SHEETY_KEY or not W_SHEETY_BEARER_AUTH:
                print("Not all environment variable are loaded.")
                return None
            W_RESPONSE = requests.get(url=W_SHEETY_URL, headers=W_SHEETY_HEADERS)
            W_RESPONSE.raise_for_status()        
            
            self.detindation_data = W_RESPONSE.json()["prices"]
        except Exception as e:
            print(f"Data:: Fail to read data from sheety-excell, msg: {e}")
            
            print("Trying local storage")
            w_data = get_destination_data_local()            
            self.detindation_data = w_data
            
        
        return self.detindation_data
        
                    

def main() -> None:
    W_FLIGHT_DATA   = DataManager()    
    w_flight_cities = W_FLIGHT_DATA.get_flight_destination_data()
    
    print(json.dumps(w_flight_cities , indent=4))            



if __name__ == "__main__":
    # print(W_SHEETY_HEADERS)
    main()