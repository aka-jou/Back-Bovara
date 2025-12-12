from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.user import User


class UserRepositoryPort(ABC):
    """Puerto de salida - Interfaz del repositorio de usuarios"""
    
    @abstractmethod
    async def save(self, user: User) -> User:
        """Guarda un usuario"""
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Busca usuario por ID"""
        pass
    
    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """Busca usuario por email"""
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Verifica si existe un usuario con ese email"""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """Actualiza un usuario"""
        pass
    
    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        """Elimina un usuario"""
        pass
