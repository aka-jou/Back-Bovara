from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from src.application.services.auth_service import AuthService
from src.application.dtos.auth_dtos import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
    MessageResponse
)
from src.infrastructure.adapters.inbound.http.dependencies import (
    get_auth_service,
    get_current_user_id
)
from src.domain.exceptions.auth_exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    InactiveUserException,
    UserNotFoundException
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea una nueva cuenta de usuario y retorna un token de acceso automáticamente"
)
async def register(
    request: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> TokenResponse:
    """
    Endpoint: Registro de usuario
    
    - Crea un nuevo usuario en el sistema
    - Genera automáticamente un token JWT
    - Retorna el token y la información del usuario
    """
    try:
        return await auth_service.register(request)
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}"
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión",
    description="Autentica un usuario y retorna un token de acceso"
)
async def login(
    request: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> TokenResponse:
    """
    Endpoint: Login de usuario
    
    - Valida las credenciales del usuario
    - Genera un nuevo token JWT
    - Retorna el token y la información del usuario
    """
    try:
        return await auth_service.login(request)
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"}
        )
    except InactiveUserException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al iniciar sesión: {str(e)}"
        )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener usuario actual",
    description="Retorna la información del usuario autenticado"
)
async def get_me(
    user_id: Annotated[str, Depends(get_current_user_id)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserResponse:
    """
    Endpoint: Obtener usuario actual
    
    - Requiere autenticación (token JWT en header)
    - Retorna la información del usuario autenticado
    """
    try:
        return await auth_service.get_current_user(user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except InactiveUserException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}"
        )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Cerrar sesión",
    description="Invalida la sesión actual (el cliente debe eliminar el token)"
)
async def logout(
    user_id: Annotated[str, Depends(get_current_user_id)]
) -> MessageResponse:
    """
    Endpoint: Logout
    
    - El cliente debe eliminar el token JWT almacenado
    - Los tokens JWT son stateless
    """
    return MessageResponse(
        message="Sesión cerrada exitosamente",
        success=True
    )
