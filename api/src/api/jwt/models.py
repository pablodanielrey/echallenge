import datetime
from typing import Any

from jose import jwt
from jose.exceptions import JWTClaimsError, JWTError

from .exceptions import JWTException, JWTInvalidFormat


class JWTManager:

    def __init__(self, key: str, algorithm: str, audience: str, issuer: str, expire: int = 30):
        self.key = key
        self.algorithm = algorithm
        self.expire = expire
        self.audience = audience
        self.issuer = issuer

    def encode_jwt(self, data: dict[str, Any]):
        if not data:
            raise JWTInvalidFormat()
        if "sub" not in data:
            raise JWTInvalidFormat()
        payload = data.copy()
        now = datetime.datetime.utcnow()
        jwt_data = {
            "iss": self.issuer,
            "aud": self.audience,
            "iat": now,
            "exp": now + datetime.timedelta(minutes=self.expire)
        }
        payload.update(jwt_data)
        ejwt = jwt.encode(payload, self.key, algorithm=self.algorithm)
        return ejwt

    def decode_jwt(self, token: str):
        try:
            payload = jwt.decode(token, self.key, algorithms=[self.algorithm], audience=self.audience, issuer=self.issuer)
            for k in ["iss", "aud", "iat", "exp"]:
                del payload[k]
            return payload
        except (JWTClaimsError, JWTError):
            raise JWTException()

