
from rest_framework_simplejwt.tokens import RefreshToken


def generate_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    acces = refresh.access_token
    acces['user_id'] = str(user.id)
    acces['role'] = str(user.role)
    return {
        "access": str(acces),
        "refresh": str(refresh)
    }
