from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.config.database import get_db
from src.infrastructure.adapters.outbound.postgres_user_repository import PostgresUserRepository
from src.infrastructure.adapters.outbound.bcrypt_password_hasher import BcryptPasswordHasher
from src.infrastructure.security.jwt_handler import JWTHandler
from src.application.services.auth_service import AuthService
from src.domain.exceptions.auth_exceptions import InvalidTokenException

# Security scheme
security = HTTPBearer()


def get_jwt_handler() -> JWTHandler:
    """Dependency: JWT Handler"""
    return JWTHandler()


def get_password_hasher() -> BcryptPasswordHasher:
    """Dependency: Password Hasher"""
    return BcryptPasswordHasher()


async def get_auth_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    jwt_handler: Annotated[JWTHandler, Depends(get_jwt_handler)],
    password_hasher: Annotated[BcryptPasswordHasher, Depends(get_password_hasher)]
) -> AuthService:
    """Dependency: Auth Service con todas sus dependencias inyectadas"""
    user_repository = PostgresUserRepository(db)
    return AuthService(
        user_repository=user_repository,
        password_hasher=password_hasher,
        jwt_handler=jwt_handler
    )


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    jwt_handler: Annotated[JWTHandler, Depends(get_jwt_handler)]
) -> str:
    """Dependency: Extrae el user_id del token JWT"""
    token = credentials.credentials
    user_id = jwt_handler.decode_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user_id
