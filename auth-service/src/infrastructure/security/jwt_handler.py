from datetime import datetime, timedelta
from typing import Tuple, Optional
from jose import jwt, JWTError
from src.infrastructure.config.settings import get_settings

settings = get_settings()


class JWTHandler:
    """Manejador de tokens JWT"""
    
    def __init__(self):
        self._secret_key = settings.SECRET_KEY
        self._algorithm = settings.ALGORITHM
        self._expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    def create_access_token(self, subject: str) -> Tuple[str, int]:
        """
        Crea un token de acceso
        Returns: (token, expires_in_seconds)
        """
        expire = datetime.utcnow() + timedelta(minutes=self._expire_minutes)
        expires_in = self._expire_minutes * 60
        
        payload = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        token = jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
        return token, expires_in
    
    def decode_token(self, token: str) -> Optional[str]:
        """
        Decodifica un token y retorna el subject (user_id)
        Returns None si el token es inválido
        """
        try:
            payload = jwt.decode(
                token, 
                self._secret_key, 
                algorithms=[self._algorithm]
            )
            return payload.get("sub")
        except JWTError:
            return None
