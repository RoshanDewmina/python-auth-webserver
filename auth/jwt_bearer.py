from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code")
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid token or expired token")
        return credentials.credentials

    def verify_jwt(self, jwt_token: str):
        payload = decodeJWT(jwt_token)
        return bool(payload)