import requests
API_KEY = "AIzaSyBG7eQfy3JPWzIKtE9RgwB2f7jCQqK2JSc"


BUSINESS_TYPES = [
    "restaurant", "cafe", "buffet", "meal_takeaway",
    "sushi", "hotel", "bakery", "store", "supermarket",
    "liquor_store", "butcher", "grocery_or_supermarket",
    "pet_store", "florist"
]

def search_business(name, region="uz", language="ru"):
    """
    Biznes nomi bo‘yicha qidirish
    Natijada faqat name va address qaytaradi
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": name,
        "region": region,
        "language": language,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data:
        return []

    results = []
    for place in data["results"]:
        if any(t in place.get("types", []) for t in BUSINESS_TYPES):
            results.append({
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "place_id": place.get("place_id")
            })

    return results


def get_details(place_id, language="uz"):
    """
    Biznes haqida to‘liq ma’lumot olish
    """
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "language": language,
        "key": API_KEY,
        "fields": "name,formatted_address,international_phone_number,address_component,geometry"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "result" not in data:
        return None

    place = data["result"]

    # Address components ichidan kerakli qismlarni olish
    region, country, district, post_index, street = None, None, None, None, None
    for comp in place.get("address_components", []):
        types = comp.get("types", [])
        if "administrative_area_level_1" in types:
            region = comp.get("long_name")
        elif "country" in types:
            country = comp.get("long_name")
        elif "administrative_area_level_2" in types or "sublocality" in types:
            district = comp.get("long_name")
        elif "postal_code" in types:
            post_index = comp.get("long_name")
        elif "route" in types or "street_address" in types or "street_number" in types:
            if street:
                street += " " + comp.get("long_name")
            else:
                street = comp.get("long_name")

    return {
        "lat": place.get("geometry", {}).get("location", {}).get("lat"),
        "lng": place.get("geometry", {}).get("location", {}).get("lng"),
        "name": place.get("name"),
        "address": place.get("formatted_address"),
        "phone": place.get("international_phone_number"),
        "region": region,
        "country": country,
        "district": district,
        "post_index": post_index,
        "street": street
    }
