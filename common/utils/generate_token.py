from datetime import timedelta

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


def generate_token_for_user(user, time=timedelta(days=30)):
    refresh = RefreshToken.for_user(user)
    acces = refresh.access_token
    acces['user_id'] = str(user.id)
    acces['role'] = str(user.role)
    return {
        "access": str(acces),
        "refresh": str(refresh)
    }
