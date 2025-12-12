# core-service/src/infrastructure/auth/jwt_handler.py
import time
from typing import Optional
from jose import JWTError, jwt

# ⚠️ IMPORTANTE: Debe ser la MISMA clave que en Auth Service
SECRET_KEY = "tu-clave-secreta-super-segura-cambiar-en-produccion-123456"
ALGORITHM = "HS256"

def decode_token(token: str) -> Optional[dict]:
    """
    Decodifica y valida un token JWT
    Retorna el payload si es válido, None si no lo es
    """
    try:
        # Decodificar token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Verificar expiración
        exp = payload.get("exp")
        if exp is None:
            print("❌ Token sin fecha de expiración")
            return None
            
        if time.time() > exp:
            print("❌ Token expirado")
            return None
        
        # Token válido
        return payload
        
    except JWTError as e:
        print(f"❌ JWT Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error decodificando token: {e}")
        return None
