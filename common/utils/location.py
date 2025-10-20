DEFAULT_LAT = 41.2995  # Tashkent latitude
DEFAULT_LON = 69.2401  # Tashkent longitude

def get_user_location(request):
    try:
        lat = float(request.query_params.get("lat", DEFAULT_LAT))
        lon = float(request.query_params.get("lon", DEFAULT_LON))
        return lat, lon
    except ValueError:
        return DEFAULT_LAT, DEFAULT_LON
