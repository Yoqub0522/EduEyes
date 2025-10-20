import math

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 4)

# common/utils/distance.py
from django.db.models import F, Value, FloatField, ExpressionWrapper
from django.db.models.functions import Radians, Sin, Cos, Sqrt, Power, Round
from django.db.models import Func

# Custom ASIN (Postgres has ASIN)
class Asin(Func):
    function = "ASIN"
    arity = 1

def annotate_distance(queryset, user_lat, user_lon, precision=2):
    """
    Annotate queryset with distance_km (in kilometers) rounded to `precision` decimals.
    user_lat,user_lon can be str or float.
    """
    try:
        lat_val = float(user_lat)
        lon_val = float(user_lon)
    except Exception:
        # fallback to Tashkent if values invalid
        lat_val = 41.2995
        lon_val = 69.2401

    lat1 = Radians(Value(lat_val))
    lon1 = Radians(Value(lon_val))
    lat2 = Radians(F("business_branch__address__lat"))
    lon2 = Radians(F("business_branch__address__long"))

    # Haversine expression
    haversine_expr = ExpressionWrapper(
        6371 * 2 *
        Asin(
            Sqrt(
                Power(Sin((lat1 - lat2) / 2), 2) +
                Cos(lat1) * Cos(lat2) *
                Power(Sin((lon1 - lon2) / 2), 2)
            )
        ),
        output_field=FloatField()
    )

    # Round to precision
    distance_expr = Round(haversine_expr, precision)

    return queryset.annotate(distance_km=distance_expr)


def format_distance(distance_km: float) -> str:
    """
    Annotated masofani foydalanuvchiga qulay formatda qaytaradi:
    < 1 km  -> "350 m"
    >= 1 km -> "1.25 km"
    """
    if distance_km is None:
        return None

    distance_m = distance_km * 1000
    if distance_m < 1000:
        return f"{int(distance_m)} m"
    return f"{round(distance_km, 2)} km"
