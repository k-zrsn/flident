### Flident

### future plans
# clickable flight number links to flightradar24
# os make alert


from FlightRadar24.api import FlightRadar24API
from time import sleep
import os


### Create variables
blank = ["N/A", "", "NONE"]
max_flights = 10
min_alt = 100 #ft
max_alt = 11000 #ft
location = [
    33.536212, #latitude
    -76.960029, #longitude
    0.0582168 #elevation km
]
radius = {
    "tl_y": 38.655159, # top left lat 
    "tl_x": -77.122887, # top left lon
    "br_y": 38.412390, # bottom right lat
    "br_x": -76.811537 # bottom right lon
}



class FlightIdent:
    def __init__(self):
        self._api = FlightRadar24API()
        self._data = {}


    def get_data(self):
        data_list = []

        try:
            bounds = self._api.get_bounds(radius)
            flights = self._api.get_flights(bounds=bounds)
            flights = sorted(
                [f for f in flights if min_alt < f.altitude < max_alt],
                key=lambda x: x.altitude,
                reverse=False 
            )   
            

            for flight in flights[:max_flights]:
                while True:
                    try: 
                        details = self._api.get_flight_details(flight)

                        try: 
                            aircraft = details["aircraft"]["model"]["text"]

                        except (KeyError, TypeError):
                            aircraft = ""


                        aircraft = aircraft 
                        origin = (flight.origin_airport_iata)
                        destination = (flight.destination_airport_iata)
                        callsign = (flight.callsign)

                        data_list.append(
                            {
                                "callsign": callsign,
                                "aircraft": aircraft,
                                "origin": origin,
                                "destination": destination,
                                "altitude": flight.altitude,
                                "speed": flight.ground_speed,
                                "hdg": flight.heading
                                
                            }
                        )

                        break

                    except (KeyError, TypeError):
                        return

            self._data = {f["callsign"]: f for f in data_list}

        except (ConnectionError):
            return 


    @property
    def data(self):
        return self._data


while True:
    if __name__ == "__main__":
        fi = FlightIdent()
        fi.get_data()

        os.system('cls')
        print("----- Flident -----")
        if not fi.data:
            print("\nNo aircraft found.\nRescan in 10 seconds.")
            sleep(10)
        else:
            print("\nCurrently flying overhead:\n")
            for i, flight in fi.data.items():
                print(
                    f"Flight {i}:\n"
                    f"  Aircraft: {flight['aircraft']}\n"
                    f"  From: {flight['origin']} -> To: {flight['destination']}\n"
                    f"  FL: {flight['altitude']} ft\n"
                    f"  GS: {flight['speed']} kts\n"
                    f"  HDG: {flight['hdg']}\n"
                )
            sleep(2)