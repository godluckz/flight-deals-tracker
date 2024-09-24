from datetime import datetime
from dateutil import tz

class ClassDateTimeUtils:    
    
    def __init__(self) -> None:
        self.utc_time_zone   = tz.tzutc()
        self.local_time_zone = tz.tzlocal()
            


    def get_date_and_time_local(self, p_utc_date_time_string: str, from_utc = False) -> tuple[str, str]:
        def get_date_and_time(p_date_time_string: str) -> tuple[str, str]:
            w_date_time_string = str(p_date_time_string)
            try:
                w_date = w_date_time_string.split("T")[0]
                w_time = w_date_time_string.split("T")[1].split("+")[0]  
            except Exception as e:
                w_date = w_date_time_string.split(" ")[0]
                w_time = w_date_time_string.split(" ")[1].split("+")[0]          
                
            return w_date, w_time        
        #--------------------------#
        # -- SUB FUNCTION ABOVE -- #
        #--------------------------#        
        w_date, w_time = get_date_and_time(p_date_time_string = p_utc_date_time_string)            
        # print(w_date, w_time)

        if from_utc:
            w_utc_datetime = datetime.strptime(f"{w_date} {w_time}", '%Y-%m-%d %H:%M:%S')
            
            # Tell the datetime object that it's in UTC time zone since     
            w_utc_datetime = w_utc_datetime.replace(tzinfo=self.utc_time_zone)    

            # Convert time zone
            w_local_datime = w_utc_datetime.astimezone(self.local_time_zone)
            # print(f"local_datime: {w_local_datime}")
            
            w_date_local, w_time_local = get_date_and_time(p_date_time_string = w_local_datime)        
        else:
            w_date_local = w_date
            w_time_local = w_time
        
        return w_date_local, w_time_local        
    
    
    def convert_datetime_from_unix_code(p_unix_code: int) -> str:
        # extract datetime from the given Unix timestamp
        w_unix_timestamp = datetime.fromtimestamp(p_unix_code)        
        w_datetime_str = w_unix_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        # print(w_datetime_str)
        return w_datetime_str