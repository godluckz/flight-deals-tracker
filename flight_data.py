class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(   self,                  
                    p_origin_city         : str, 
                    p_origin_airport      : str, 
                    p_destination_city    : str, 
                    p_destination_airport : str, 
                    p_out_date            : str, 
                    p_return_date         : str,
                    p_price               : float) -> None:
        self.origin_airport       = p_origin_airport
        self.origin_city          = p_origin_city
        self.destination_city     = p_destination_city
        self.destination_airport  = p_destination_airport
        self.out_date             = p_out_date
        self.return_date          = p_return_date
        self.price               :float = round(p_price,2)
        
        
        
def main() -> None:
    raise NotImplementedError("'main' is not implemented.")


if __name__ == "__main__":
    main()    