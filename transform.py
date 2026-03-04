
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