import jwt
from datetime import datetime, timedelta, timezone
from decouple import config

JWT_SECRET = config('JWT_SECRET', default="mysecretkey")

def signJWT(user_id: str) -> str:
    """
    Sign a JWT token with the user_id as the payload.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc)+ timedelta(minutes=15)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def decodeJWT(token: str) -> dict:
    """
    Decode a JWT token and return the payload.
    """
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None