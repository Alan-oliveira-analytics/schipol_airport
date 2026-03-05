

def transform_aircraft_types(aircraft_types_pages):

    result = []
    aircraft_types = []

    for page in aircraft_types_pages:
        aircraft_types.extend(page.get("aircraftTypes"))

    for aircraft in aircraft_types:
        result.append({
            "iataMain": aircraft.get("iataMain"),
            "iataSub": aircraft.get("iataSub"),
            "description": aircraft.get("longDescription")
        })


    return result
    



def transform_airlines(airlines_pages):

    result = []
    airlines = []

    for page in airlines_pages:
        airlines.extend(page.get("airlines"))


    for airline in airlines:
        result.append({
            "iata": airline.get("iata"),
            "icao": airline.get("icao"),
            "nvls": airline.get("nvls"),
            "name": airline.get("publicName")
        })

    return result



def transform_destinations(destinations_pages):
    
    result = []
    destinations = []

    for page in destinations_pages:
        destinations.extend(page.get("destinations"))


    for destination in destinations:

        name = destination.get("publicName")

        if name:
            name = name.get("english")
        

        result.append({
            "name": name,
            "country": destination.get("country"),
            "iata": destination.get("iata"),
            "city": destination.get("city")
        })

    return result