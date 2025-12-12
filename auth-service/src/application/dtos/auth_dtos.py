from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class RegisterRequest(BaseModel):
    """DTO para solicitud de registro"""
    email: EmailStr
    password: str
    full_name: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@bovara.com",
                "password": "password123",
                "full_name": "Usuario Ejemplo"
            }
        }
    )


class LoginRequest(BaseModel):
    """DTO para solicitud de login"""
    email: EmailStr
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@bovara.com",
                "password": "password123"
            }
        }
    )


class UserResponse(BaseModel):
    """DTO para respuesta con datos de usuario"""
    id: str
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_entity(cls, user):
        """Crea UserResponse desde entidad User"""
        return cls(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at
        )
    
    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """DTO para respuesta de autenticación con token"""
    access_token: str
    expires_in: int
    user: UserResponse
    token_type: str = "bearer"
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "user@bovara.com",
                    "full_name": "Usuario Ejemplo",
                    "is_active": True,
                    "is_superuser": False,
                    "created_at": "2025-12-06T23:00:00"
                }
            }
        }
    )


class AuthResponse(BaseModel):
    """DTO para respuesta de autenticación (alternativo)"""
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponse


class MessageResponse(BaseModel):
    """DTO de respuesta genérica"""
    message: str
    success: bool = True
    
    # auth-service/src/schemas/user.py

# Agregar este schema:
class UserWithTokenResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str
