from src.domain.entities.user import User
from src.domain.ports.user_repository_port import UserRepositoryPort
from src.domain.ports.password_hasher_port import PasswordHasherPort
from src.domain.exceptions.auth_exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidCredentialsException,
    InactiveUserException
)
from src.application.dtos.auth_dtos import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse
)
from src.infrastructure.security.jwt_handler import JWTHandler


class AuthService:
    """Servicio de aplicación - Casos de uso de autenticación"""
    
    def __init__(
        self,
        user_repository: UserRepositoryPort,
        password_hasher: PasswordHasherPort,
        jwt_handler: JWTHandler
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._jwt_handler = jwt_handler
    
    async def register(self, request: RegisterRequest) -> TokenResponse:
        """Caso de uso: Registrar nuevo usuario"""
        
        # Verificar si el usuario ya existe
        if await self._user_repository.exists_by_email(request.email):
            raise UserAlreadyExistsException(request.email)
        
        # Hashear contraseña
        hashed_password = self._password_hasher.hash(request.password)
        
        # Crear entidad de usuario
        user = User.create(
            email=request.email,
            hashed_password=hashed_password,
            full_name=request.full_name
        )
        
        # Persistir usuario
        saved_user = await self._user_repository.save(user)
        
        # Generar token
        access_token, expires_in = self._jwt_handler.create_access_token(
            subject=saved_user.id
        )
        
        return TokenResponse(
            access_token=access_token,
            expires_in=expires_in,
            user=UserResponse(
                id=saved_user.id,
                email=saved_user.email,
                full_name=saved_user.full_name,
                is_active=saved_user.is_active,
                is_superuser=saved_user.is_superuser,
                created_at=saved_user.created_at
            )
        )
    
    async def login(self, request: LoginRequest) -> TokenResponse:
        """Caso de uso: Iniciar sesión"""
        
        # Buscar usuario por email
        user = await self._user_repository.find_by_email(request.email)
        
        if not user:
            raise InvalidCredentialsException()
        
        # Verificar contraseña
        if not self._password_hasher.verify(request.password, user.hashed_password):
            raise InvalidCredentialsException()
        
        # Verificar si está activo
        if not user.is_active:
            raise InactiveUserException()
        
        # Generar token
        access_token, expires_in = self._jwt_handler.create_access_token(
            subject=user.id
        )
        
        return TokenResponse(
            access_token=access_token,
            expires_in=expires_in,
            user=UserResponse(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                created_at=user.created_at
            )
        )
    
    async def get_current_user(self, user_id: str) -> UserResponse:
        """Caso de uso: Obtener usuario actual"""
        
        user = await self._user_repository.find_by_id(user_id)
        
        if not user:
            raise UserNotFoundException(user_id)
        
        if not user.is_active:
            raise InactiveUserException()
        
        return UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at
        )
