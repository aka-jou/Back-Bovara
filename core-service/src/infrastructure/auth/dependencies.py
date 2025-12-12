# core-service/src/infrastructure/auth/dependencies.py
from fastapi import Depends, HTTPException, status
from uuid import UUID

from .auth_bearer import verify_token

class UserAuth:
    """Modelo simplificado de usuario para autenticación"""
    def __init__(self, id: UUID, email: str = ""):
        self.id = id
        self.email = email

def get_current_user(token_data: dict = Depends(verify_token)) -> UserAuth:
    """
    Dependency para obtener el usuario actual desde el token JWT.
    """
    try:
        user_id_str = token_data.get("sub")
        
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: no contiene user_id"
            )
        
        user_id = UUID(user_id_str)
        user = UserAuth(id=user_id)
        
        print(f"✅ Usuario autenticado: {user_id}")
        return user
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: user_id malformado"
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error al procesar autenticación"
        )
